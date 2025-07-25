import sys
import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

# Rich console setup
console = Console()

# Load environment variables (optional but safe practice)
load_dotenv()

# Go 3 levels up from this file to reach ai_agent_course/
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(root_path)

# Now import from llm/config.py at root
from llm.config import openai_key

# Setup OpenAI client
client = AsyncOpenAI(api_key=openai_key)

async def get_llm_response(system_message_content: str | None, user_message_content: str) -> str:
    """
    Get a response from the LLM given system and user messages.
    Uses the gpt-4.1-nano model.
    """
    messages = []
    if system_message_content:
        messages.append({"role": "system", "content": system_message_content})
    messages.append({"role": "user", "content": user_message_content})

    try:
        response = await client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

async def zero_shot_classification_task(): 
    system_message = ( 
        "You are 'SupportAI-Classifier', an expert AI assistant. " 
        "Your task is to classify the following customer query into one of these exact categories: " 
        "'Billing Inquiry', 'Technical Issue', 'Feature Request', 'Account Cancellation'. " 
        "Output only the category name and nothing else." 
    ) 
 
    queries = { 
        "q1": "My payment didn't go through, can you check?", 
        "q2": "The app crashes every time I click the 'export' button.", 
        "q3": "It would be great if you could add a dark mode to the interface.", 
        "q4": "How do I close my account and get a refund for the remaining period?", # Touches on cancellation and billing 
        "q5": "The website is slow today when I try to log in.", 
        "q6": "I want to upgrade my subscription plan." # Potentially 'Billing Inquiry' or a new category 
    } 

    console.rule("[bold cyan] Zero Shot Prompting Task")
    for q_id, query_text in queries.items():
        classification = await get_llm_response(system_message_content = system_message, user_message_content=query_text)
        console.print(Markdown(f"Query ({q_id}): \"{query_text}\" -> Classified as: {classification}"))


if __name__ == "__main__":
    asyncio.run(zero_shot_classification_task())
