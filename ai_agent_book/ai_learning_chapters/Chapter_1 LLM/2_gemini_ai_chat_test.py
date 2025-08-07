import sys
import os

# Go 2 levels up from topic_1.4 → ai_agent_book → ai_agent_course
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)
# Now you can import from llm.config
from llm.config import google_key
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)

print(response.text)