"""Descriptions API"""
from typing import Optional
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Extra, Field  # pylint: disable=(no-name-in-module # false-positive

LOGGER = logging.getLogger(__name__)

router = APIRouter()  # These endpoints are public


# FIXME: Move to libpvarki
class ProductDescription(BaseModel):  # pylint: disable=too-few-public-methods
    """Description of a product"""

    shortname: str = Field(description="Short name for the product, used as slug/key in dicts and urls")
    title: str = Field(description="Fancy name for the product")
    icon: Optional[str] = Field(description="URL for icon")
    description: str = Field(description="Short-ish description of the product")
    language: str = Field(description="Language of this response")

    class Config:  # pylint: disable=too-few-public-methods
        """Pydantic configs"""

        extra = Extra.forbid


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
