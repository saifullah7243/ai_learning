from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

# Load the pre-trained model
model_name: str = "all-MiniLM-L6-v2"

try:
    model = SentenceTransformer(model_name)
    print(f"Model '{model_name}' loaded successfully.")
except Exception as e:
    print(f"Failed to load model '{model_name}': {e}")
    print("Ensure you have the 'sentence-transformers' library installed and the model is available.")
    exit()

# 2 Example sentences to generate embeddings
sentences: List[str] = [ 
    "The weather is sunny and warm today.", 
    "It's a beautiful day for a walk in the park.", 
    "I need to buy groceries: milk, eggs, and bread.", 
    "Financial markets reacted to the new inflation report." 
]

# Generate embeddings for the sentences
try:
    embeddings = model.encode(sentences)
except Exception as e:
    print(f"Failed to generate embeddings: {e}")
    exit()

# print information about the embeddings
print(f"Generated embeddings for {len(sentences)} sentences.")
for i, sentence in enumerate(sentences):
    print(f"Sentence: {sentence}")
    print(f"Embedding (first 5 dimensions): {embeddings[i][:5]}")
    print(f"Embedding shape: {embeddings[i].shape}")

# Example: emnbedding for the first sentence
print("\nExample embedding for the first sentence:")
first_embedding = embeddings[0] 
print(f"\nFull embedding for the first sentence (shape {first_embedding.shape}):") 
print(first_embedding) 

print(f"\nDimensionality of embeddings: {model.get_sentence_embedding_dimension()}") 
print(f"Max sequence length for this model: {model.max_seq_length} tokens") 
print("\nSuccessfully generated embeddings!")