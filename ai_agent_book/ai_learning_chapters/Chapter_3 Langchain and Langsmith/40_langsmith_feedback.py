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

client = Client()

run_id = "b8e11b9a-9cf3-49e4-985b-07e8e5936d2d"

client.create_feedback(
    run_id=run_id,
    key = "user_score",
    score=1,
    comment = "User clicked the 'looks good' button"

)