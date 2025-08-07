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

from langsmith import Client 
 
def create_gmail_dataset(): 
    client = Client() 
    dataset_name = "Gmail Classification (Eval V1)" 
     
    # Check if dataset exists to avoid duplicates 
    try: 
        dataset = client.read_dataset(dataset_name=dataset_name) 
        print(f"Dataset '{dataset_name}' already exists.") 
        return 
    except (Exception): # LangSmith client throws a generic error if not found 
        pass 
 
    dataset = client.create_dataset( 
        dataset_name=dataset_name, 
        description="A test suite for classifying emails as Primary, Spam, or Actionable." 
    ) 
 
    # Add examples to the dataset 
    client.create_examples( 
        inputs=[ 
            {"email_text": "Hi Bob, can you please send me the report by EOD Friday? Thanks, Alice."}, 
            {"email_text": "URGENT: Your account has been compromised! Click here to secure it NOW!"}, 
            {"email_text": "Hey, just checking in. Hope you have a great weekend!"}, 
            {"email_text": "Confirming your dinner reservation for 2 at The Grand Bistro tonight at 8 PM."}, 
        ], 
        outputs=[ 
            {"expected_category": "Actionable"}, 
            {"expected_category": "Spam"}, 
            {"expected_category": "Primary"}, 
            {"expected_category": "Primary"}, 
        ], 
        dataset_id=dataset.id, 
    ) 
    print(f"Successfully created dataset '{dataset_name}' with 4 examples.") 
 
if __name__ == "__main__": 
    create_gmail_dataset()