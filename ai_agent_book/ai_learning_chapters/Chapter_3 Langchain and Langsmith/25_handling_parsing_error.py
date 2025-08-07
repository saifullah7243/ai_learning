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
from langchain.output_parsers.retry import RetryWithErrorOutputParser 




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

# Create the retry parser, wrapping our original Pydantic parser 
retry_parser = RetryWithErrorOutputParser.from_llm( 
    parser=parser, 
    llm=ChatOpenAI(model="gpt-4.1-mini", temperature=0) # LLM to use for fixing errors 
) 

## Ceate the chain..
retry_chain = prompt | model | retry_parser 

 
