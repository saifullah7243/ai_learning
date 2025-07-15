try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Error: The 'sentence-transformers' library is not installed.")
    print("Please install it using: pip install sentence-transformers")
    exit()
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

# 1. Load a pre-trained SentenceTransformer model
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # 2. Define a list of example sentences
    sentences = [
        "The cat sits on the mat.",
        "A feline is resting upon the rug.",     # Semantically similar to sentence 1
        "It is raining heavily today.",          # Different topic
        "What is the current weather like?"      # A question related to sentence 3
    ]

    print("Generating embeddings...")
    embeddings = model.encode(sentences)
    print(f"Embeddings shape: {embeddings.shape}")  # Should be (4, 384)

    # 3. Set the first sentence as the query
    query_embedding = embeddings[0]
    corpus_embeddings = embeddings[1:]
    query_embedding_2d = query_embedding.reshape(1, -1)

    # 4. Cosine Similarity
    cos_sim_scores = cosine_similarity(query_embedding_2d, corpus_embeddings)
    print("\nCosine Similarity Scores (Query vs Corpus):")
    for i, score in enumerate(cos_sim_scores[0]):
        print(f"  Query vs Sentence {i+2} ('{sentences[i+1]}'): {score:.4f}")

    # 5. Euclidean Distance
    euclidean_dist_scores = euclidean_distances(query_embedding_2d, corpus_embeddings)
    print("\nEuclidean Distances (Query vs Corpus):")
    for i, dist in enumerate(euclidean_dist_scores[0]):
        print(f"  Query vs Sentence {i+2} ('{sentences[i+1]}'): {dist:.4f}")

    # 6. Dot Product (MiniLM produces normalized vectors)
    print("\nDot Product Scores (Query vs Corpus - assuming normalized embeddings):")
    for i, doc_embedding in enumerate(corpus_embeddings):
        dot_product_score = np.dot(query_embedding, doc_embedding)
        print(f"  Query vs Sentence {i+2} ('{sentences[i+1]}'): {dot_product_score:.4f}")
except Exception as e:
    print(f"An error occurred: {e}")

# Optional: Manual normalization for safety (if unsure embeddings are normalized)
# query_norm = query_embedding / np.linalg.norm(query_embedding)
# corpus_norms = [emb / np.linalg.norm(emb) for emb in corpus_embeddings]
# dot_product_normalized = np.dot(query_norm, corpus_norms[0])
# print(f"\nDot product (manually normalized) with first sentence: {dot_product_normalized:.4f}"