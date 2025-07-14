import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys
openai_key = os.getenv("OPENAI_API_KEY")
google_key = os.getenv("GOOGLE_API_KEY")


assert openai_key
assert google_key
