import sys
import os
import asyncio
from typing import List, Dict, Any

from openai import AsyncOpenAI, OpenAIError
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

# Rich console setup
console = Console()

# Load environment variables from .env
load_dotenv()

# Go 3 levels up to reach the root path of ai_agent_course/
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(root_path)

# Now import from llm/config.py at root level
try:
    from llm.config import openai_key
except ImportError:
    console.print("[bold red]Error:[/bold red] Could not import `openai_key` from llm.config")
    sys.exit(1)

# Setup OpenAI async client
client = AsyncOpenAI(api_key=openai_key)

# Define the message format
messages_dialogue_style: List[Dict[str, str]] = [
    {"role": "system", "content": "You are a helpful brainstorming assistant for marketing slogans."},
    {"role": "user", "content": "Suggest three slogans for a new brand of eco-friendly coffee."}
]


async def main() -> None:
    try:
        console.rule("[bold cyan]First Response")
        assistant_response_1 = await client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages_dialogue_style,
            temperature=0.3
        )
        first_reply: str = assistant_response_1.choices[0].message.content
        console.print(Markdown(first_reply))

        # Add assistant reply to messages
        messages_dialogue_style.append({"role": "assistant", "content": first_reply})

        # Add user follow-up
        messages_dialogue_style.append({
            "role": "user",
            "content": "I like the first one. Can you make it punchier and highlight the 'freshness' aspect?"
        })

        console.rule("[bold blue]Second Response")
        assistant_response_2 = await client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages_dialogue_style,
            temperature=0.3
        )
        second_reply: str = assistant_response_2.choices[0].message.content
        console.print(Markdown(second_reply))

    except OpenAIError as e:
        console.print(f"[bold red]OpenAI API Error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {e}")


# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
