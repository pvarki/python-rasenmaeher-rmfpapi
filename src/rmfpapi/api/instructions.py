"""Instructions endpoints"""
from typing import Dict
import logging
import json
from pathlib import Path

from fastapi import APIRouter, Depends
from libpvarki.middleware import MTLSHeader
from libpvarki.schemas.product import UserCRUDRequest

LOGGER = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(MTLSHeader(auto_error=True))])


@router.post("/{language}")
async def user_intructions(user: UserCRUDRequest) -> Dict[str, str]:
    """return user instructions"""
    instructions_json_file = Path("/opt/templates/rune-fake.json")
    
    tak_instructions_data = json.loads(instructions_json_file.read_text(encoding="utf-8"))
    
    return {"callsign": user.callsign, "instructions": json.dumps(tak_instructions_data), "language": language}
    