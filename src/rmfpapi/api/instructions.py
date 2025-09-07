"""Instructions endpoints"""

from typing import Dict
import logging
import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from libpvarki.middleware import MTLSHeader
from libpvarki.schemas.product import UserCRUDRequest

from ..config import load_manifest

LOGGER = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(MTLSHeader(auto_error=True))])


@router.get("/assets/{file_path:path}")
async def get_asset(file_path: str) -> FileResponse:
    """Asset file"""
    basepath = Path("/opt/templates/assets")
    assetpath = basepath / file_path
    LOGGER.info("Looking for {} from {}".format(file_path, assetpath))
    if not assetpath.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=str(assetpath))


@router.post("/{language}")
async def user_intructions(user: UserCRUDRequest, language: str) -> Dict[str, str]:
    """return user instructions"""
    instructions_json_file = Path("/opt/templates/rune-fake.json")
    manifest = load_manifest()

    instructions_text = instructions_json_file.read_text(encoding="utf-8")
    instructions_text = instructions_text.replace(
        "__FAKE_ASSETS__", f"{manifest['product']['api']}api/v1/instructions/assets"
    )
    instructions_data = json.loads(instructions_text)

    return {"callsign": user.callsign, "instructions": instructions_data, "language": language}
