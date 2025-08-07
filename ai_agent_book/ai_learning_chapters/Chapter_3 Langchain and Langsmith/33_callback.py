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
from langchain.callbacks.stdout import StdOutCallbackHandler

async def main():
    """
    Demonstrates the use of a built-in callback handler to observe chain execution. 
    """
    ## 1 define the handler
    ## This handler will print all events to standard output
    stdout_handler = StdOutCallbackHandler()

    ## 2 Define the simple chain
    prompt = ChatPromptTemplate.from_template(
        "Tell me short about the inspiring story about{subject}"
    )

    model = ChatOpenAI(model = "gpt-4.1-nano", temperature = 0.3)

    chain = prompt | model

    print("--- Invoking chain with StdOutCallbackHandler ---")

    ## 3 invoke the chain with callback handler in the config
    config:RunnableConfig = {"callbacks":[stdout_handler]}

    response = await chain.ainvoke({"subject":"AI Developer"}, config=config)

    print("\n-- Chain execution finished ---")
    print(f"\n Final Response content: \n{response.content}")

if __name__ == "__main__":
    asyncio.run(main())