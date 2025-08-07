import sys
import os
from dotenv import load_dotenv

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config

# Load .env variables and config
load_dotenv()
config = load_config()
openai_key = config.openai_key

import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langsmith import Client
from langchain_core.runnables import RunnablePassthrough
from custom_evaluator import check_category_match
from typing import Dict, Any

## Chain definition
def create_classification_chain(prompt_template:str, model:ChatOpenAI)->Dict:
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | model | StrOutputParser()
    return RunnablePassthrough.assign(category = chain)

async def main():
    client = Client()

    dataset_name = "Gmail Classification (Eval V1)"
    model = ChatOpenAI(
        model="gpt-4.1-nano",
        temperature=0.7,
        max_tokens=1024
    )

    # prompt 1
    prompt_v1 = "Classify the following email into one of three categories: Primary, Spam, or Actionable.\n\nEmail: {email_text}\n\nCategory:"
    chain_v1 = create_classification_chain(prompt_v1, model)
    
    # prompt 2
    prompt_v2 = """ 
    You are an email classification expert. Your task is to classify an email into exactly one of the 
    following three categories: 
    - Primary: A standard, non-urgent personal or professional message. 
    - Spam: An unsolicited marketing or malicious email. 
    - Actionable: An email that explicitly requires the recipient to perform a task. 
     
    Respond with a single word only. 
 
    Email: {email_text} 
    Category: 
    """ 
    chain_v2 = create_classification_chain(prompt_v2, model) 

    # Run evaluation test for prompt v1
    print("Running evaluation for Prompt V1...")
    client.run_on_dataset(
        dataset_name=dataset_name,
        llm_or_chain_factory = lambda: chain_v1,
        custom_evaluators = [check_category_match],
        project_name="gmail-assistant-eval-v1",
        concurrency_level=5
    )

    # Run evaluation test for prompt v2
    print("Running evaluation for Prompt V2...")
    client.run_on_dataset(
        dataset_name=dataset_name,
        llm_or_chain_factory = lambda: chain_v2,
        custom_evaluators = [check_category_match],
        project_name="gmail-assistant-eval-v2",
        concurrency_level=5
    )
    print("Evaluation completed for both prompts.")

if __name__ == "__main__":
    asyncio.run(main())
