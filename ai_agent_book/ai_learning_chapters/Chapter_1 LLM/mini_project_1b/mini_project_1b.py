###Part -1: Import necessary libraries and set up the environment
# Import libraries
import numpy as np 
from sentence_transformers import SentenceTransformer 
from sklearn.metrics.pairwise import cosine_similarity 
import faiss

### Data
corpus = [ 
"Our company offers a comprehensive healthcare plan for all full-time employees.", 
"Employees are entitled to 20 paid vacation days per year.", 
"The new software update includes enhanced security features and a revamped user interface.", 
"Quarterly financial reports indicate a 15% growth in revenue.", 
"For technical support, please email support@examplecorp.com or call our helpline.", 
"The healthcare benefits package covers medical, dental, and vision insurance.", # Similar to sentence 1 
"To request time off, submit a form through the employee portal at least two weeks in advance.", # Related to sentence 2 
"Security protocols have been upgraded across all company platforms following the recent patch.", # Similar to sentence 3 
"Our customer service team is available 24/7 to assist with any issues." # Related to sentence 5 
] 

query = "What are the healthcare benefits?"

### Part -2: Embedding generation
# Load an embedding model:
model_name = 'all-MiniLM-L6-v2' # Fast and good for this scale 
print(f"Loading embedding model: {model_name}...") 
model = SentenceTransformer(model_name) 

# Embed the corpus and the query: 
print("Embedding corpus...") 
corpus_embeddings = model.encode(corpus, convert_to_tensor=False).astype('float32')  # Get as NumPy arrays 
print("Embedding query...") 
query_embedding = model.encode(query, convert_to_tensor=False).astype('float32')

print(f"Corpus embeddings shape: {corpus_embeddings.shape}") # (num_sentences, embedding_dim) 
print(f"Query embedding shape: {query_embedding.shape}")   # (embedding_dim,) or (1, embedding_dim) 

### Part -3: Calculate similarity and Retrieval
# Calculate cosine similarity between the query embedding and all corpus embeddings. 
# Reshape query_embedding to 2D if it's 1D for cosine_similarity function 
if query_embedding.ndim == 1: 
  query_embedding_2d = query_embedding.reshape(1, -1) 
else: 
  query_embedding_2d = query_embedding 
similarities = cosine_similarity(query_embedding_2d, corpus_embeddings) 
# similarities is a 2D array, e.g., [[s1, s2, s3, ...]] so we take the first row 
similarity_scores = similarities[0] 

# Find the top N most similar sentences: 
top_k = 3 
# Get indices of top_k scores in descending order 
# np.argsort returns indices that would sort the array in ascending order. 
# So we use a negative sign to sort in descending effectively, then take top_k. 
sorted_indices = np.argsort(-similarity_scores) 
top_k_indices = sorted_indices[:top_k] 
print(f"\nQuery: \"{query}\"") 
print(f"\nTop {top_k} most similar sentences from the corpus:") 
for i, index in enumerate(top_k_indices): 
  print(f"  {i+1}. \"{corpus[index]}\" (Score: {similarity_scores[index]:.4f})") 