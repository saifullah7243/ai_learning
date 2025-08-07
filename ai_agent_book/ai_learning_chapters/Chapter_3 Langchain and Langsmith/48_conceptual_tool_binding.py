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

import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

from calendar_tools import check_calendar_availability

async def run_with_tool():
    tools = [check_calendar_availability]

    model = ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0.3
    )

    model_with_tools = model.bind_tools(tools)

    # first query
    user_query = "Hey, can we meet tomorrow at 2:30 PM PST to discuss the project?"
    print(f"User: {user_query}")


    ## model decided to call the tool
    ai_response = await model_with_tools.ainvoke([HumanMessage(content=user_query)])

    print(f"AI: {ai_response}")

if __name__ == "__main__":
    asyncio.run(run_with_tool())