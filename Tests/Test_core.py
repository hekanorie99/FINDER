import pytest

from phone_osint.core import investigate


@pytest.mark.asyncio
async def test_normalize_valid():
    r = await investigate("+79991234567")
    assert r.e164 == "+79991234567"
    assert r.valid is True
    assert r.country  # Russia


@pytest.mark.asyncio
async def test_invalid_number():
    r = await investigate("+7999")
    assert r.valid is False
