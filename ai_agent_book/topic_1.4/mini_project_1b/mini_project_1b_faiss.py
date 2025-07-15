import numpy as np
from typing import List

# Check for sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Error: The 'sentence-transformers' library is not installed.")
    print("Please install it using: pip install sentence-transformers")
    exit()

# Check for faiss
try:
    import faiss
except ImportError:
    print("Error: The 'faiss' library is not installed.")
    print("Please install it using: pip install faiss-cpu")
    exit()

# Define corpus with type hint
corpus: List[str] = [
    "Our company offers a comprehensive healthcare plan for all full-time employees.",
    "Employees are entitled to 20 paid vacation days per year.",
    "The new software update includes enhanced security features and a revamped user interface.",
    "Quarterly financial reports indicate a 15% growth in revenue.",
    "For technical support, please email support@examplecorp.com or call our helpline.",
    "The healthcare benefits package covers medical, dental, and vision insurance.",
    "To request time off, submit a form through the employee portal at least two weeks in advance.",
    "Security protocols have been upgraded across all company platforms following the recent patch.",
    "Our customer service team is available 24/7 to assist with any issues."
]

# Define query with type hint
query: str = "What are the medical advantages?"

try:
    model_name = 'all-MiniLM-L6-v2'
    print(f"Loading embedding model: {model_name}...")
    model = SentenceTransformer(model_name)

    corpus_embeddings = model.encode(corpus, convert_to_tensor=False)
    query_embedding = model.encode(query, convert_to_tensor=False)

    corpus_embeddings_np = np.array(corpus_embeddings).astype('float32')
    query_embedding_np = np.array(query_embedding).astype('float32')

    if query_embedding_np.ndim == 1:
        query_embedding_np = query_embedding_np.reshape(1, -1)

    dimension = corpus_embeddings_np.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(corpus_embeddings_np)

    k = 3
    distances, faiss_indices = index.search(query_embedding_np, k)

    print(f"\nQuery: \"{query}\"")
    print(f"\nTop {k} most similar sentences from FAISS:")
    for i in range(k):
        doc_index = faiss_indices[0][i]
        score = distances[0][i]
        print(f"  {i+1}. \"{corpus[doc_index]}\" (Score: {score:.4f})")

except Exception as e:
    print(f"An error occurred: {e}")
    exit()
