from pydantic import Field, BaseModel
from typing import List, Optional
from enum import Enum

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
