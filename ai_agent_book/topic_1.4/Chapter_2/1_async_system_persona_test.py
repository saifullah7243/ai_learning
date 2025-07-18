import sys
import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

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
    Uses the gpt-4o model.
    """
    messages = []
    if system_message_content:
        messages.append({"role": "system", "content": system_message_content})
    messages.append({"role": "user", "content": user_message_content})

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

async def main():
    user_question = "Tell me about the challenges faced during the late Roman Republic"
    
    console.rule("[bold cyan] Response with No System Persona")
    response_generic = await get_llm_response(None, user_question)
    console.print(Markdown(response_generic))

    console.rule("[bold cyan]Response with Detailed System Persona")
    expert_persona = (
        "You are Dr. Livius, an esteemed Professor of Ancient History at Oxford University, "
        "specializing in the socio-political dynamics of the late Roman Republic. "
        "Your explanations are detailed, nuanced, and draw upon primary historical sources where appropriate, "
        "but are articulated for an intelligent layperson. You avoid overly simplistic narratives."
    )
    response_expert = await get_llm_response(expert_persona, user_question)
    console.print(Markdown(response_expert))

if __name__ == "__main__":
    asyncio.run(main())
