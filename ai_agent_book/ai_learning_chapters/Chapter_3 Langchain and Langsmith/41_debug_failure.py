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

from typing import List, Optional 
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate 
from pydantic import BaseModel, Field 
from langchain_core.output_parsers import PydanticOutputParser 
from dotenv import load_dotenv 
import asyncio

# Define our desired structured output 
class ActionItem(BaseModel): 
    task: str = Field(description="The specific action item to be completed.") 
    assignee: Optional[str] = Field(description="The person or team assigned to the task.") 
    deadline: Optional[str] = Field(description="The deadline for the action item.")

class ActionItems(BaseModel): 
    items: List[ActionItem]


async def run_failing_chain(): 
    # Setup the parser 
    parser = PydanticOutputParser(pydantic_object=ActionItems) 

     # A prompt that includes the format instructions from the parser 
    prompt = ChatPromptTemplate.from_messages([ 
        ("system", "You are an expert at extracting action items from text. Please respond with a JSON object containing the action items, formatted according to the provided schema."), 
        ("human", "From this email, please extract all action items.\n\nEmail: {email_text}\n\n{format_instructions}") 
    ]).partial(format_instructions=parser.get_format_instructions())

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0) 
    chain = prompt | model | parser 

      # An ambiguous email that might not have clear action items 
    ambiguous_email = "Hey team, just thinking about the project. We should probably consider the new marketing angles soon. Also, someone should look into the Q3 budget. Thanks."

    print("Invoking chain that might fail...") 
    try: 
        response = await chain.with_config({"tags": ["debugging-test"]}).ainvoke({"email_text": ambiguous_email}) 
        print("Success!", response) 
    except Exception as e: 
        print("Chain failed!") 
        print(f"Error: {e}") 

if __name__ == "__main__":
    asyncio.run(run_failing_chain())
