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
chat_model = ChatOpenAI(model="gpt-4.1-mini", temperature=0.1)

# Define the prompt template
prompt_template = ChatPromptTemplate.from_template(
    "Explain the concept of '{user_topic}' in one concise paragraph, suitable for a beginner."
)

# Define the output parser
str_parser = StrOutputParser()

# Construct the chain
explanation_chain = prompt_template | chat_model | str_parser

# Async single invoke
async def main_async_invoke():
    print("\n--- Async Single Invoke ---")
    topic_input = {"user_topic": "Tiktok"}
    try:
        result_async_single = await explanation_chain.ainvoke(topic_input)
        print(f"Async Single Invoke Result: {result_async_single}")
    except Exception as e:
        print(f"Error in async single invoke: {e}")

# Async batch invocation
async def main_async_batch():
    print("\n\n--- Async Batch Invoke ---")
    input_batch = [
        {"user_topic": "Tree"},
        {"user_topic": "Root"}
    ]
    try:
        result_async_batch = await explanation_chain.abatch(input_batch)
        print("Async Batch Results:")
        for i, res in enumerate(result_async_batch):
            print(f"Input: {input_batch[i]['user_topic']}, Output: {res[:50]}...")
    except Exception as e:
        print(f"Error in async batch invoke: {e}")

# Main entry point
if __name__ == "__main__":
    # Ensure OPENAI_API_KEY is set before running
    if os.getenv("OPENAI_API_KEY"):
        asyncio.run(main_async_invoke())
        asyncio.run(main_async_batch())
    else:
        print("Skipping async examples as API key is not set.")
