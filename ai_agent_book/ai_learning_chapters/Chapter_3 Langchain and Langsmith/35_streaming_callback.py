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
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler

async def main():
    """Demonstrates programmatic access to a token stream using AsyncIteratorCallbackHandler."""

    ## 1 Initialize the handler
    streaming_handler = AsyncIteratorCallbackHandler()
    ## 2 define the chain
    propmt = ChatPromptTemplate.from_template(
        "Write the 3 lines of poem about {topic}"
    )
    model = ChatOpenAI(
        model = "gpt-4.1-nano",
        streaming = True, 
        temperature = 0.1
    )

    ## Make the chian
    chain = propmt | model

    ## Prepare the cofig
    config:RunnableConfig = {"callbacks":[streaming_handler]}

    print("--- Starting streaming chain ---")
    async def invoke_chain():
        await chain.ainvoke({"topic":"The Ocean"}, config=config)
    task = asyncio.create_task(invoke_chain())

    # 5 consume the stream from the handler's iterator
    full_response = ""
    async for token in streaming_handler.aiter():
        print(token, end="", flush=True)
        full_response += token

    ## wait for the background task to complete 
    await task

    print("\n\n--- Streaming finished ---") 
    print(f"Full response assembled: \n{full_response}")

if __name__ == "__main__":
    asyncio.run(main()) 


