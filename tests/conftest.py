"""pytest automagics"""
import logging
import os

from libpvarki.logging import init_logging

# Default is "ecs" and it's not great for tests
os.environ["LOG_CONSOLE_FORMATTER"] = "local"
init_logging(logging.DEBUG)
LOGGER = logging.getLogger(__name__)
