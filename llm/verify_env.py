import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY") or ""
google_key = os.getenv("GOOGLE_API_KEY") or ""



print(f"OpenAI key length: {len(openai_key)}")
print(f"Google key length: {len(google_key)}")
