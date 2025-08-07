import sys
import os
import asyncio

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load API key
config = load_config()
openai_key = config.openai_key

# LangChain setup
chat_model = ChatOpenAI(model="gpt-4.1-nano", temperature=0.5)

# Define the prompt template
prompt_template = ChatPromptTemplate.from_template(
    "Explain the concept of '{user_topic}' in one concise paragraph, suitable for a beginner."
)

# Define the output parser
str_parser = StrOutputParser()

# Construct the chain
explanation_chain = prompt_template | chat_model | str_parser

# Synchronous streaming function
def run_sync_stream():
    input_sync = {"user_topic":"Business"}
    print("Synchronous Streaming")
    try:
        for chunk in explanation_chain.stream(input_sync):
            print(chunk, end="", flush=True)
        print()  
    except Exception as e:
        print(f"Error in sync stream: {e}")


# Asynchronous streaming function
import asyncio
async def run_async_stream():
    print("Asynchronous Streaming")
    input_async = {"user_topic":"Internship"}

    try:
        async for chunk in explanation_chain.astream(input_async):
            print(chunk, end="", flush=True)
        print()  # newline
    except Exception as e:
        print(f"Error in async stream: {e}")



if __name__ == "__main__":
    if os.getenv("OPENAI_API_KEY"):
        # Change topics here or make dynamic
        run_sync_stream()
        asyncio.run(run_async_stream())
    else:
        print("Skipping streaming examples — OPENAI_API_KEY not set.")


# import asyncio

# # Synchronous Streaming
# print("\n--- Synchronous Streaming ---")
# try:
#     print(f"Streaming explanation for 'photosynthesis':")
#     for chunk in explanation_chain.stream({"user_topic": "Business"}):
#         print(chunk, end="", flush=True)
#     print()  # Newline after streaming is complete
# except Exception as e:
#     print(f"Error in sync stream: {e}")

# # Asynchronous Streaming
# async def main_async_stream():
#     print("\n--- Asynchronous Streaming ---")
#     try:
#         print(f"Async streaming explanation for 'solar flares':")
#         async for chunk in explanation_chain.astream({"user_topic": "Internship"}):
#             print(chunk, end="", flush=True)
#         print()  # Newline
#     except Exception as e:
#         print(f"Error in async stream: {e}")

# if __name__ == "__main__":
#     if os.getenv("OPENAI_API_KEY"):
#         # Run sync stream example directly
#         print(f"Streaming explanation for 'photosynthesis':")
#         for chunk in explanation_chain.stream({"user_topic": "photosynthesis"}):
#             print(chunk, end="", flush=True)
#         print()

#         # Run async stream example
#         asyncio.run(main_async_stream())
#     else:
#         print("Skipping streaming examples as API key is not set.")

