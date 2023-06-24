"""Endpoints for information for the end-user"""
import logging

from fastapi import APIRouter, Depends
from libpvarki.middleware import MTLSHeader

from .schema import UserInstructionFragment, UserCRUDRequest


LOGGER = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(MTLSHeader(auto_error=True))])


@router.post("/fragment")
async def client_instruction_fragment(user: UserCRUDRequest) -> UserInstructionFragment:
    """Return user instructions, we use POST because the integration layer might not keep
    track of callsigns and certs by UUID and will probably need both for the instructions"""
    _ = user
    # TODO: use Jinja template
    result = UserInstructionFragment(html="<p>Hello, World!</p>")
    return result
