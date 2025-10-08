import os
import json
from sentence_transformers import SentenceTransformer

# 1. Load a pre-trained Sentence Transformer model
# We use the same model that we'll use in the browser later.
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Define the path to your content and the output file
content_dir = '_posts'
output_file = '_site/static/model/embeddings.json'

# 3. A list to hold all of our chunk and embedding objects
documents = []

# 4. Process each text file in the content directory
for filename in os.listdir(content_dir):
    if filename.endswith('.md'):
        filepath = os.path.join(content_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

            # Split the text into paragraphs (or chunks)
            # A simple split by double newline is effective for blogs.
            chunks = text.split('\n\n')
            
            # 5. Generate embeddings for each chunk
            print(f"Generating embeddings for {filename}...")
            embeddings = model.encode(chunks)

            # 6. Store each chunk and its corresponding embedding
            for i, chunk in enumerate(chunks):
                # Skip empty chunks
                if chunk.strip():
                    documents.append({
                        'chunk': chunk,
                        'embedding': embeddings[i].tolist() # Convert numpy array to a standard list
                    })

# 7. Write the final list of documents to the JSON file
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, 'w') as f:
    json.dump(documents, f, indent=2)

print(f"✅ Successfully created {output_file} with {len(documents)} document chunks.")