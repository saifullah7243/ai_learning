from pydantic.v1 import BaseModel, Field
import datetime

### Step 1: Define the Tool's Arguments with Pydantic 
class CalendarCheckInput(BaseModel):
    iso_datetime:str = Field(description="The proposed meeting time in ISO 8601 format, e.g., '2025-07-04T14:30:00'.")
    duration_minutes: int = Field(description="The duration of meeting in minuts, default=30")

### Step 2: Create the Asynchronous Tool Function 
import asyncio
from langchain_core.tools import tool

@tool(args_schema=CalendarCheckInput)
async def check_calendar_availability(iso_datetime: str, duration_minutes: int = 30)-> str:
    """ 
    Checks if a given time slot is available in the user's calendar.  
    Use this to verify meeting times before scheduling them. 
    """ 
    ## Mock implementation for checking calendar availability
    print(f"\n---\nTOOL: Checking calendar for {iso_datetime} ({duration_minutes} mins)...")

    try:
        requested_time = datetime.datetime.fromisoformat(iso_datetime)
        # Mocking saome busy solts
        busy_slots = [
            datetime.datetime(2025, 7, 4, 14, 0),  # Busy from 14:00 to 14:30
            datetime.datetime(2025, 7, 4, 15, 0)   # Busy from 15:00 to 15:30
        ]

        is_busy = any(
            busy_time <= requested_time < busy_time + datetime.timedelta(minutes=60)
            for busy_time in busy_slots
        )
        if is_busy: 
            print("TOOL: Slot is busy.") 
            return f"The time slot at {iso_datetime} is not available. The user has another event." 
        else: 
            print("TOOL: Slot is available.") 
            return f"The time slot at {iso_datetime} is available for a {duration_minutes} minute meeting."
        
    except ValueError as e:
         return "Error: The provided datetime is not in a valid ISO 8601 format." 
    except Exception as e:
        return f"An unexpected error occurred: {e}"

