import sys
import os
from dotenv import load_dotenv

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config

# Load .env variables and config
load_dotenv()
config = load_config()
openai_key = config.openai_key

from pydantic import BaseModel, Field
import datetime
import asyncio
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import ToolMessage

### Step 1: Define the Tool's Arguments with Pydantic 
class CalendarCheckInput(BaseModel):
    iso_datetime:str = Field(description="The proposed meeting time in ISO 8601 format, e.g., '2025-07-04T14:30:00'.")
    duration_minutes: int = Field(description="The duration of meeting in minuts, default=30")

### Step 2: Create the Asynchronous Tool Function 

@tool(args_schema=CalendarCheckInput)
async def check_calendar_availability(iso_datetime: str, duration_minutes: int = 30)-> str:
    """
    Crucial Docstring for LLM to understand the tool - use the below format

    What it does: A function that checks if a given time slot is available in the user's calendar.  
    When to use it: Use this to verify meeting times before scheduling them.

    Additional information:  
    - The input is a string in ISO 8601 format  
    - Timeslots are based on the duration provided in minutes  
    - The output is a string indicating whether the time slot is available or not
    """ 
    ## Mock implementation for checking calendar availability
    print(f"\n---\nTOOL: Checking calendar for {iso_datetime} ({duration_minutes} mins)...")

    try:
        requested_time = datetime.datetime.fromisoformat(iso_datetime)
        pkt = datetime.timezone(datetime.timedelta(hours=5))  # Pakistan Standard Time (PKT)
        requested_time = requested_time.astimezone(pkt)  # Convert to PKT
        # Mocking saome busy solts
        busy_slots = [
            datetime.datetime(2025, 7, 4, 14, 0, tzinfo=pkt),  # Busy from 14:00 to 14:30
            datetime.datetime(2025, 7, 4, 15, 0, tzinfo=pkt)   # Busy from 15:00 to 15:30
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
    

## Main function to test the tool
async def main():
    # bind the tool to the LLM
    tool = [check_calendar_availability]
    model = ChatOpenAI(
        model = 'gpt-4.1-nano',
        temperature = 0.2
    )

    model_with_tool = model.bind_tools(tool)

    # Create the prompt
    prompt = PromptTemplate.from_template("Can you check the calendar availability at 2:30 PM PKT for me?")

    # create the intial chain
    chain = prompt | model_with_tool

    ## Step-1: Invoke the chain to get LLM's response (which may include the tool call)
    print("=" * 50)
    print("Step-1: Sending query to LLM....")
    print("=" * 50)

    initial_response = await chain.ainvoke({})
    print(f"LLM response Type: {type(initial_response)}")

    ## Initialize a list to store all messages in the conversation
    messages = [initial_response]

    ## Track tool call state
    tool_call_count = 0
    tool_name_called = []

    ## Step-2: Check if the LLM wants to use tools
    while messages[-1].tool_calls:
        print("\n" + "=" * 50) 
        print(f"STEP 2: LLM requested tool calls...") 
        print("=" * 50) 

        # Get the tool calls from the last message
        tool_calls = messages[-1].tool_calls
        print(f"Number of tool calls requested: {len(tool_calls)}")

        ## Step-3: Execuste each tool call
        for tool_call in tool_calls:
            tool_call_count += 1
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            tool_name_called.append(tool_name)

            print(f"\nTool Call #{tool_call_count}:") 
            print(f"  Tool Name: {tool_name}") 
            print(f"  Arguments: {tool_args}")

            # Execute the tool (in this case, check_calendar_availability)
            if tool_name ==  "check_calendar_availability":
                result = await check_calendar_availability.ainvoke(tool_args)
            else:
                result = f"Unknown tool: {tool_name}"
            
            print(f"Result: {result}")

            ## Create a tool message with the result
            tool_message = ToolMessage(
                content = result,
                tool_call_id = tool_call["id"],
                name = tool_name
            )
            messages.append(tool_message)
         # Step 4: Send the tool results back to the LLM for final response 
        print("\n" + "=" * 50) 
        print("STEP 3: Sending tool results back to LLM...") 
        print("=" * 50) 

        ## continue the conversation with all messages (including tool call)
        followup_response = await model.ainvoke(messages)
        messages.append(followup_response)

        ## check if the llm wants to call mpre tools(loop contninues if yes)
        ## check if no tools were called(llm gave direct response)
    if tool_call_count == 0:
        print("\n" + "=" * 50) 
        print("LLM did not call any tools, giving direct response...") 
        print("=" * 50)
    
    ## step 5 Print the final response and statistics
    print("\n" + "=" * 50)
    print("Final Response from LLM:")
    print("=" * 50)
    print(messages[-1].content)

    print("\n" + "=" * 50) 
    print("TOOL CALL STATISTICS:") 
    print("=" * 50) 
    print(f"Total tool calls: {tool_call_count}") 
    print(f"Tools used: {', '.join(set(tool_name_called))}") 
    print(f"Tool call sequence: {' -> '.join(tool_name_called) if tool_name_called else 'None'}") 




if __name__ == "__main__":
    asyncio.run(main())