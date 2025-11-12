"""Endpoints for information for the end-user"""

import base64
import logging
from typing import List
from fastapi import APIRouter, Depends
from libpvarki.middleware import MTLSHeader
from libpvarki.schemas.product import UserCRUDRequest
from pydantic import BaseModel, Field
from rmfpapi.api.clientinfo import zip_pem

LOGGER = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(MTLSHeader(auto_error=True))])


class ClientInstructionData(BaseModel):  # pylint: disable=too-few-public-methods
    """Represents a single ZIP file containing mission data or product instructions."""

    title: str = Field(..., description="Original filename or title of the zip file.")
    filename: str = Field(..., description="Filename used for download, includes user callsign.")
    data: str = Field(
        ..., description="Base64-encoded zip file contents", examples=["data:application/zip;base64,UEsDBBQAAAAI..."]
    )

    class Config:  # pylint: disable=too-few-public-methods
        """Pydantic configs"""

        extra = "forbid"


# TODO move to libpvarki
class ClientInstructionResponse(BaseModel):  # pylint: disable=too-few-public-methods
    """Response schema for returning client mission instructions."""

    data: List[ClientInstructionData] = Field(..., description="Container object for returned data.")

    class Config:  # pylint: disable=too-few-public-methods
        """Pydantic configs"""

        extra = "forbid"


@router.post("/data", response_model=ClientInstructionResponse)
async def client_instruction_data(user: UserCRUDRequest) -> ClientInstructionResponse:
    """Return user instructions, we use POST because the integration layer might not keep
    track of callsigns and certs by UUID and will probably need both for the instructions"""
    zip1_bytes = zip_pem(user.x509cert, f"{user.callsign}_1.pem")
    zip2_bytes = zip_pem(user.x509cert, f"{user.callsign}_2.pem")

    return ClientInstructionResponse(
        data=[
            ClientInstructionData(
                title="iFake",
                data=f"data:application/zip;base64,{base64.b64encode(zip1_bytes).decode('ascii')}",
                filename=f"{user.callsign}_1.zip",
            ),
            ClientInstructionData(
                title="aFake",
                data=f"data:application/zip;base64,{base64.b64encode(zip2_bytes).decode('ascii')}",
                filename=f"{user.callsign}_2.zip",
            ),
        ]
    )
