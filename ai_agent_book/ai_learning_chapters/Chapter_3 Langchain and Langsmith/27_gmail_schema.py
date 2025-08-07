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

## Creat the Entity Extraction Schema using pydantic
class ExtractedEntity(BaseModel):
    text:str = Field(description="The acutal text that extracted entity (e.g., 'Project Phoenix', 'next Tuesday')")
    type:str = Field(description="The type of the entity (e.g., 'Project Name', 'Date', 'Person').")

## Create the Action Item Schema using Pydantic
class ActionItem(BaseModel):
    description:str = Field(description="A clear and concise description of the task")
    due_date:Optional[str] = Field(None, description="The suggested due date for the action, if any, in YYYY-MM-DD format.")
    assignee:Optional[str] = Field(None, description="The person or team assigned to the task, if mentioned.")

## Create the Processed Email Schema using Pydantic
class ProcessedEmail(BaseModel):
    category:EmailCategory = Field(description="The main classification of the email.")
    subject:str = Field(description="The subject line of the email")
    summary:str = Field(description="A one-sentence summary of the email's content.")
    entities:List[ExtractedEntity] = Field(description="A list of key named entities found in the email.")
    action_items: List[ActionItem] = Field(description="A list of specific action items or tasks requested in the email.") 
    sentiment: str = Field(description="The overall sentiment of the email (e.g., 'Positive', 'Neutral', 'Negative').") 

## Let's create am example instance to see how it looks 
example_processed_email = ProcessedEmail( 
    category=EmailCategory.ACTIONABLE, 
    subject="Project Phoenix - Next Steps", 
    summary="Alice requires the final report by next Tuesday to prepare for the client meeting.", 
    entities=[ 
        ExtractedEntity(text="Alice", type="Person"), 
        ExtractedEntity(text="Project Phoenix", type="Project Name"), 
        ExtractedEntity(text="next Tuesday", type="Date") 
    ], 
    action_items=[ 
        ActionItem( 
            description="Prepare the final report for Project Phoenix.", 
            due_date="2025-06-17", 
            assignee="Me" 
        ), 
        ActionItem( 
            description="Send the report to Alice.", 
            due_date="2025-06-17", 
            assignee="Me" 
        ) 
    ], 
    sentiment="Neutral"
)

print(example_processed_email.model_dump_json(indent=2))

## 1_ Create the Parser for full schema
full_parser = PydanticOutputParser(pydantic_object = ProcessedEmail)
full_format_instructions = full_parser.get_format_instructions()

## 2_ Creat the Prompt
full_prompt = ChatPromptTemplate.from_template( 
            """You are a hyper-efficient and accurate email processing agent. 
            Analyze the provided email and extract the required information precisely according to 
            the following JSON schema. 
            Do not add any commentary or introductory text. Your output must be only the valid 
            JSON object. 
            JSON Schema: 
            {format_instructions} 
            Email to Analyze: --- 
            From: {sender} 
            Subject: {subject} 
            Body: 
            {body} --- 
""" ).partial(format_instructions = full_format_instructions)

## 3 Model 
model = ChatOpenAI(model="gpt-4.1-mini", temperature = 0.2)

## 4 Fulll email chain
full_email_processing_chain = full_prompt | model | full_parser 

## 5 Invoking the chain
complex_email = { 
    "sender": "alice@corporate.com", 
    "subject": "Urgent Action: Finalize Q2 'Project Dragon' Report", 
    "body": """Hi team, 
        This is a critical reminder that the final report for Project Dragon needs to be submitted to me by this Friday, June 20th, 2025. 
        The report should include a full summary of our findings and a list of key achievements. Bob, please ensure your data tables are included. 
        The client presentation is scheduled for next Monday. This report is essential for that meeting. 
        Thanks, 
        Alice 
    """ 
} 
try:
    if openai_key:
        processed_result = full_email_processing_chain.invoke(complex_email)
        print("\n---- Full Email Processing Result (a Json)---")
        print(processed_result.model_dump_json(indent=2)) 
except Exception as e:
    print("An Error Occured during the chain:{e}")

