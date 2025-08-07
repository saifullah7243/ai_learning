import pytest
from calendar_tools import check_calendar_availability

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

## Availability Tests
async def test_availability_for_free_slot():
    """Tests the tool's response for a known available time."""
    result = await check_calendar_availability.ainvoke({
        "iso_datetime": "2025-07-04T12:00:00",
        "duration_minutes": 60
    })
    assert "is available" in result
    assert "60 minute" in result

## Busy Slot Tests
async def test_availability_for_busy_slot():
    """Tests the tool's response for a known busy time."""
    result = await check_calendar_availability.ainvoke({
        "iso_datetime": "2025-06-25T14:30:00"
    })
    assert "is not available" in result

## invalid input tests
async def test_invalid_datetime_format():
    """Tests the tool's error handling for malformed input."""
    result = await check_calendar_availability.ainvoke({
        "iso_datetime": "July 4th, 2025 at noon"  # Invalid ISO format
    })
    assert "Error: The provided datetime is not in a valid ISO 8601 format." in result

