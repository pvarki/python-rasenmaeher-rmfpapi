"""Configurations with .env support"""
from starlette.config import Config

cfg = Config(".env")

LOG_LEVEL: int = cfg("LOG_LEVEL", default=20, cast=int)
