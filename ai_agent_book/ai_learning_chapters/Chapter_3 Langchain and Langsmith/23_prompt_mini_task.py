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

## Creat the Entity Extraction Schema using pydantic
class ExtractedEntity(BaseModel):
    text:str = Field(description="The acutal text that extracted entity (e.g., 'Project Phoenix', 'next Tuesday')")
    type:str = Field(description="The type of the entity (e.g., 'Project Name', 'Date', 'Person').")

## Create the Action Item Schema using Pydantic
class ActionItem(BaseModel):
    description:str = Field(description="A clear and concise description of the task")
    due_date:Optional[str] = Field(None, description="The suggested due date for the action, if any, in YYYY-MM-DD format.")
    assignee:Optional[str] = Field(None, description="The person or team assigned to the task, if mentioned.")

# ## Create the Processed Email Schema using Pydantic
# class ProcessedEmail(BaseModel):
#     category:EmailCategory = Field(description="The main classification of the email.")
#     subject:str = Field(description="The subject line of the email")
#     summary:str = Field(description="A one-sentence summary of the email's content.")
#     entities:List[ExtractedEntity] = Field(description="A list of key named entities found in the email.")
#     action_items: List[ActionItem] = Field(description="A list of specific action items or tasks requested in the email.") 
#     sentiment: str = Field(description="The overall sentiment of the email (e.g., 'Positive', 'Neutral', 'Negative').") 

class SimpleClassification(BaseModel): 
    category: EmailCategory = Field(description="The main classification of the email.") 
    confidence: float = Field(description="A confidence score between 0.0 and 1.0 for the classification.") 

# 1. Create an instance of the parser for our desired schema 
parser = PydanticOutputParser(pydantic_object=SimpleClassification)

# 2. Get the format instructions 
format_instructions = parser.get_format_instructions() 
# print(format_instructions)

email_classification_template = ChatPromptTemplate.from_messages([
    ("system", 
     """You are an expert email analysis assistant. Your task is to analyze an email 
            and classify it into one of the following categories: Primary, Spam, Actionable, or Promotional.

            You must provide your response in a JSON format that adheres to the following schema.

            Do NOT include any other text, explanations, or apologies. Only the JSON object.
            {format_instructions}"""
                ),
                ("human", 
                """Please analyze the following email:

            From: {sender}
            Subject: {subject}
            Body:
            {body}"""
                )
])

## Use partial()
final_prompt_template = email_classification_template.partial(format_instructions=format_instructions)

## Create the chain
model = ChatOpenAI(model="gpt-4.1-nano", temperature=0) 
classification_chain = final_prompt_template | model | parser 

## Lets check with sample
sample_email = { 
    "sender": "newsletter@promo.com", 
    "subject": "50% OFF EVERYTHING! Don't Miss Out!", 
    "body": "Our biggest sale of the year is here! Click now to shop deals on all your favorite products. This offer ends Friday." 
} 

try:
    if os.getenv("OPENAI_API_KEY"): 
        result = classification_chain.invoke(sample_email)

        print("\n--- Email Classification Result ---")
        print(f"Category: {result.category}")
        print(f"Confidence: {result.confidence}")
        print(f"Type of result: {type(result)}")
    else:
        print("OPENAI_API_KEY not found in environment variables.")
except Exception as e:
    print(f"Error during chain invocation: {e}")
