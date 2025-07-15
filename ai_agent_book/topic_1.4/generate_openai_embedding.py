import sys
import os

# Go 2 levels up from topic_1.4 → ai_agent_book → ai_agent_course
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(root_path)
# Now you can import from llm.config
from llm.config import openai_key

from openai import OpenAI

try: 
    client = OpenAI()
    client.models.list() 
except Exception as e:
    print(f"Failed to connect to OpenAI API: {e}")
    print("Ensure you have the 'openai' library installed and your API key is set correctly.")
    exit()

model_id = "text-embedding-3-small" 

texts_to_embed = [ 
    "The quick brown fox jumps over the lazy dog.", 
    "Exploring the capabilities of AI embeddings.", 
    "Hivemind: Building the future of AI agents." 
]

print(f"Request embeddings for {len(texts_to_embed)} texta using model:{model_id}\n")
try:
    response = client.embeddings.create(
        model=model_id,
        input=texts_to_embed
    )

    all_embeddings = []
    for i, emb_objext in enumerate(response.data):
        print(f"Text: {texts_to_embed[i]}")
        print(f"Embedding (first 5 values): {emb_objext.embedding[:5]}")
        all_embeddings.append(emb_objext.embedding)
        print("_" * 20)

    # Model usage and information
    print(f"\nModel used: {response.model}")
    print(f"Total tokens used: {response.usage.total_tokens}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")

except Exception as e: 
    print(f"An error occurred: {e}") 