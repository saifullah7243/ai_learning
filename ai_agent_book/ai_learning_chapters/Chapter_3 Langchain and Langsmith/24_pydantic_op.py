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
from pydantic import Field, BaseModel
from typing import List, Optional
from enum import Enum
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate



# Load .env variables and config
load_dotenv()
config = load_config()
openai_key = config.openai_key


# Creat the email category using Enum
class EmailCategory(str, Enum):
    PRIMARY = "Primary"
    SPAM = "Spam"
    ACTIONABLE = "Actionable"
    PROMOTIONAL = "Promtional"

class ClassifiedEmail(BaseModel):
    category:EmailCategory = Field(description="The Final classification of the email")
    reasoning:str = Field(description="A brief explnantion for the chosen category")

## Create the parser and get instruction
parser = PydanticOutputParser(pydantic_object = ClassifiedEmail)
format_instruction = parser.get_format_instructions()

## Create the prompt template with instsriuction
prompt = ChatPromptTemplate.from_template( 
"""Analyze the email below and classify it. 
{format_instructions} 
Email Body: 
{email_body}""" 
).partial(format_instructions=format_instruction) 

## Instantiate the model
model = ChatOpenAI(model="gpt-4.1-nano", temperature=0) 


## Assemble the Chain 
chain = prompt | model | parser 

### Invoke to chain
email_to_classify = "Hi team, please remember to submit your quarterly reports by EOD Friday. This is mandatory for all departments. Thanks, Management."

try: 
    if os.getenv("OPENAI_API_KEY"): 
      
        result = chain.invoke({"email_body": email_to_classify})        
        print("--- Parsed Output ---") 
        print(f"Type: {type(result)}") 
        print(f"Category: {result.category.value}") # Access enum value 
        print(f"Reasoning: {result.reasoning}") 
except Exception as e: 
      print(f"An error occurred: {e}") 