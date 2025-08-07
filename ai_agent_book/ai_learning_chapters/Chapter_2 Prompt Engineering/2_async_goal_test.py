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

# Ensure project root (ai_agent_book/) is in sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)

# Import config loader from utils
from utils.config_loader import load_config
config = load_config()
openai_key = config.openai_key

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
            max_tokens=250,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

async def recipe_formatting_task():
    recipe_text = """ 
    Simple Guacamole: 
    To make this delicious dip, you'll need 2 ripe avocados, 1/2 small onion (finely chopped),  
    1 lime (juiced), salt to taste, and a pinch of cumin.  
    First, mash the avocados in a bowl. Then, stir in the chopped onion, lime juice, salt, and cumin.  
    Mix well and serve immediately with tortilla chips. 
    """ 
    system_chef_persona = "You are 'Chef Quick-Recipe', an expert at clearly presenting recipe information."
    # Prompt 1: Paragraph output 
    goal_paragraph = ( 
        "From the following recipe text, please extract the ingredients and the preparation steps. " 
        "Present the ingredients in a short paragraph and the cooking instructions in another paragraph."  
    )
    prompt1_user_content = f"Recipe Text:\n{recipe_text}\n\nTask: {goal_paragraph}"

    console.rule("[bold cyan] Recipe Formatting Task - Paragraph Output")
    response_generic = await get_llm_response(system_message_content=system_chef_persona, user_message_content=prompt1_user_content)
    console.print(Markdown(response_generic))

    # Prompt 2: List output 
    goal_list = ( 
        "From the following recipe text, please extract the ingredients and the preparation steps. " 
        "Present the ingredients as a bulleted list, including quantities. " 
        "Present the cooking instructions as a numbered list." 
    ) 
    prompt2_user_content = f"Recipe Text:\n{recipe_text}\n\nTask: {goal_list}" 

    console.rule("[bold cyan] Recipe Formatting Task - List Output")
    response_expert = await get_llm_response(system_message_content=system_chef_persona, user_message_content=prompt2_user_content)
    console.print(Markdown(response_expert))

if __name__ == "__main__":
    asyncio.run(recipe_formatting_task())
