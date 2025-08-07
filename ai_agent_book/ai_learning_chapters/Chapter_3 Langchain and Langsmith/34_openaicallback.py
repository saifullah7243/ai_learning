import sys
import os
import asyncio
from dotenv import load_dotenv

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config

# Load .env variables and config
load_dotenv()
config = load_config()
openai_key = config.openai_key

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_community.callbacks.openai_info import OpenAICallbackHandler


async def main():
    prompt = ChatPromptTemplate.from_template(
        "Expian the concpt of {topic} in one paragrapg"
    )

    model = ChatOpenAI(model="gpt-4.1-nano", temperature = 0.1)

    chain = prompt | model


    ## The handler can be used as a contect manager
    cost_handler = OpenAICallbackHandler()
    config = {"callbacks":[cost_handler]}

     
    response = await chain.ainvoke({"topic":"Black Hole"}, config=config)

    print("\n--- Cost and Token Information ---") 
    print(f"Total Tokens: {cost_handler.total_tokens}") 
    print(f"Prompt Tokens: {cost_handler.prompt_tokens}") 
    print(f"Completion Tokens: {cost_handler.completion_tokens}") 
    print(f"Total Cost (USD): ${cost_handler.total_cost:.6f}") 


if __name__ == "__main__":
    asyncio.run(main())


