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

from langsmith import traceable
from langchain_openai import ChatOpenAI 
from langchain_core.prompts import ChatPromptTemplate

@traceable(run_type="tool", name="Clean Email Text V2")
def clean_email_text(raw_text: str) -> str:
    # Implement your email cleaning logic here
    cleaned_text = raw_text.split("---")[0].strip().lower()
    return cleaned_text

async def run_traceable_chain():
    model = ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0.1,
        max_tokens=1024
    )

    prompt = ChatPromptTemplate.from_template("Summarize this: {cleaned_text}")

    chain = {
        "cleaned_text": lambda x: clean_email_text(x["raw_email"]),
    } | prompt | model

    email_with_signature = "This is the core message.\n---\nRegards, Bob\nLegal Disclaimer: ... "
    print("Invoking chain with traceable function...")
    response = await chain.ainvoke({"raw_email": email_with_signature})
    print("Response:", response)

if __name__ == "__main__":
    asyncio.run(run_traceable_chain())
