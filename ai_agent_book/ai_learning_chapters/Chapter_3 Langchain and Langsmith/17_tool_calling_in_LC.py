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
from pydantic import BaseModel, Field
from typing import Optional, List

# Load .env variables and config
load_dotenv()
config = load_config()
openai_key = config.openai_key


model = ChatOpenAI(
    model = "gpt-4.1-nano",
    temperature = 0.1
)

## Define schema:
class UserProfile(BaseModel):
    user_name: str = Field(description="The user's unique username.")
    user_id: int = Field(description="The user's integer ID")
    email: Optional[str] = Field(None, description="The user's Optional email address")
    interests: List[str] = Field(description="A list of the user's interest")

## Configured model to return str output
str_llm = model.with_structured_output(UserProfile)

if os.getenv("OPENAI_API_KEY"):
    print("\n--- Structured Output Example ---")

    user_description = (
        "The user is jsmith, their ID is 9988. They love rock climbing, "
        "sci-fi novels, and their email is jsmith@example.com."
    )

    structured_response = str_llm.invoke(user_description)

    print("Type of response:", type(structured_response))
    print("\nStructured Response (as Pydantic object):")
    print(structured_response)

    print("\nAccessing data:")
    print(f"Username: {structured_response.user_name}")
    print(f"Interests: {structured_response.interests}")

    print("\nJSON representation:")
    print(structured_response.model_dump_json(indent=2))

else:
    print("Skipping structured output example as API key is not set.")

