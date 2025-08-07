from openai import OpenAI
from config import openai_key
import sys

# Initialize client
client = OpenAI(api_key=openai_key)

# Send request with streaming
response = client.chat.completions.create(
    model="gpt-4.1-nano",  # your custom or fine-tuned model
    messages=[{"role": "user", "content": "Writes the 10 ides about business in details?"}],
    max_tokens=50,
    temperature=0.7,
    stream=True
)

# Stream and print
print("Streaming response:")
for chunk in response:
    delta = chunk.choices[0].delta
    if delta.content:
        sys.stdout.write(delta.content)
        sys.stdout.flush()

print("\nDone.")
