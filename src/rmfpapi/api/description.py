"""Descriptions API"""
import logging

from fastapi import APIRouter, HTTPException
from libpvarki.schemas.product import ProductDescription

LOGGER = logging.getLogger(__name__)

router = APIRouter()  # These endpoints are public


@router.get(
    "/{language}",
    response_model=ProductDescription,
)
async def return_product_description(language: str) -> ProductDescription:
    """Fetch description from each product in manifest"""
    LOGGER.debug("Got language: {}".format(language))
    if language == "fi":
        return ProductDescription(
            shortname="fake",
            title="Feikkituote",
            icon=None,
            description=""""tuote" integraatioiden testaamiseen""",
            language="fi",
        )
    if language == "en":
        return ProductDescription(
            shortname="fake",
            title="Fake Product",
            icon=None,
            description="Fake product for integrations testing and examples",
            language="en",
        )
    # NOTE: Generally should return just the default language but this is for testing purposes
    raise HTTPException(status_code=404)
