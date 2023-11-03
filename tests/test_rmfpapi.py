"""Package level tests"""
from rmfpapi import __version__


def test_version() -> None:
    """Make sure version matches expected"""
    assert __version__ == "0.5.0"
