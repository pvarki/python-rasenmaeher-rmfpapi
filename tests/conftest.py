"""pytest automagics"""
from typing import Generator
import logging
import os

from libpvarki.logging import init_logging
import pytest
from fastapi.testclient import TestClient

from rmfpapi.app import get_app

# Default is "ecs" and it's not great for tests
os.environ["LOG_CONSOLE_FORMATTER"] = "local"
init_logging(logging.DEBUG)
LOGGER = logging.getLogger(__name__)
APP = get_app()


@pytest.fixture
def mtlsclient() -> Generator[TestClient, None, None]:
    """Fake the NGinx header"""
    client = TestClient(
        APP,
        headers={
            "X-ClientCert-DN": "CN=harjoitus1.pvarki.fi,O=harjoitus1.pvarki.fi,L=KeskiSuomi,ST=Jyvaskyla,C=FI",
        },
    )
    yield client
