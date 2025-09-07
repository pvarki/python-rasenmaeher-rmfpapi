"""Configurations with .env support"""
from typing import Dict, Any, cast
from pathlib import Path
import functools
import json
import logging

from starlette.config import Config

LOGGER = logging.getLogger(__name__)

cfg = Config()  # not supporting .env files anymore because https://github.com/encode/starlette/discussions/2446

LOG_LEVEL: int = cfg("LOG_LEVEL", default=20, cast=int)
TEMPLATES_PATH: Path = cfg("TEMPLATES_PATH", cast=Path, default=Path(__file__).parent / "templates")


@functools.cache
def load_manifest(filepth: Path = Path("/pvarki/kraftwerk-init.json")) -> Dict[str, Any]:
    """Load the manifest"""
    if not filepth.exists():
        # return a dummy manifest
        LOGGER.warning("Returning dummy manifest")
        rm_uri = "https://localmaeher.dev.pvarki.fi"
        mtls_uri = rm_uri.replace("https://", "https://mtls.")
        return {
            "deployment": "localmaeher",
            "rasenmaeher": {
                "init": {"base_uri": rm_uri, "csr_jwt": "LOL, no"},
                "mtls": {"base_uri": mtls_uri},
                "certcn": "rasenmaeher",
            },
            "product": {"dns": "fake.localmaeher.dev.pvarki.fi"},
        }
    return cast(Dict[str, Any], json.loads(filepth.read_text(encoding="utf-8")))
