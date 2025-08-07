import sys
import os
import asyncio
from dotenv import load_dotenv

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load .env variables and config
load_dotenv()
config = load_config()
openai_key = config.openai_key

# Initialize the model
model = ChatOpenAI(
    model="gpt-4.1-nano",  
    temperature=0.1
)

async def call_model():
    messages = [
        SystemMessage(content="You are a terse and witty tech commentator"),
        HumanMessage(content="What is your opinion on the future of AI?")
    ]

    # --- Synchronous call ---
    print("--- Sync Call ---")
    sync_response = model.invoke(messages)
    print(sync_response.content)

    # --- Asynchronous call ---
    print("--- Async Call ---")
    async_response = await model.ainvoke(messages)
    print(async_response.content)

    # --- Asynchronous streaming call ---
    print("--- Async Streaming Call ---")
    async for chunk in model.astream(messages):
        print(chunk.content, end="", flush=True)
    print()

if __name__ == "__main__":
    if os.getenv("OPENAI_API_KEY"):
        asyncio.run(call_model())
    else:
        print("Skipping direct model call example as API key is not set.")
