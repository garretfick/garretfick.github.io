import os
import json
import re
import yaml
from sentence_transformers import SentenceTransformer

# 1. Load pre-trained Sentence Transformer models
model_minilm = SentenceTransformer('all-MiniLM-L6-v2')
model_bge = SentenceTransformer('BAAI/bge-small-en-v1.5')

# 2. Define the path to your content and the output files
content_dir = '_posts'
output_file_minilm = '_site/static/model/embeddings-all-MiniLM-L6-v2.json'
output_file_bge = '_site/static/model/embeddings-bge-small-en-v1.5.json'

# 3. Chunking parameters
MAX_CHUNK_WORDS = 400  # Maximum words per chunk
OVERLAP_WORDS = 100    # Words to overlap between chunks

# 4. A list to hold all chunks with titles for embedding
all_chunks = []        # Original chunks (without title prefix)
all_chunks_with_title = []  # Chunks with title prefix (for embedding)

def split_by_headers(content):
    """Split content by markdown headers, returning list of (header, text) tuples."""
    # Match markdown headers (## or ### etc.)
    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

    sections = []
    last_end = 0
    current_header = ""

    for match in header_pattern.finditer(content):
        # Save previous section
        if match.start() > last_end:
            text = content[last_end:match.start()].strip()
            if text:
                sections.append((current_header, text))

        # Start new section with this header
        current_header = match.group(0)  # Full header line
        last_end = match.end()

    # Add final section
    if last_end < len(content):
        text = content[last_end:].strip()
        if text:
            sections.append((current_header, text))

    return sections

def split_large_section(text, max_words, overlap_words):
    """Split a large text section into smaller chunks with overlap."""
    words = text.split()

    if len(words) <= max_words:
        return [text]

    chunks = []
    start = 0

    while start < len(words):
        end = start + max_words
        chunk_words = words[start:end]
        chunks.append(' '.join(chunk_words))

        # Move start forward, accounting for overlap
        if end >= len(words):
            break
        start = end - overlap_words

    return chunks

def create_chunks_from_content(content, max_words, overlap_words):
    """Create chunks from content, splitting by headers and enforcing size limits."""
    sections = split_by_headers(content)

    # If no headers found, treat entire content as one section
    if not sections:
        sections = [("", content)]

    all_chunks = []

    for header, text in sections:
        # Combine header with text
        section_text = f"{header}\n\n{text}" if header else text

        # Count words
        word_count = len(section_text.split())

        if word_count <= max_words:
            # Section fits in one chunk
            all_chunks.append(section_text)
        else:
            # Split large section
            sub_chunks = split_large_section(text, max_words, overlap_words)

            # Add header to each sub-chunk
            for sub_chunk in sub_chunks:
                chunk_with_header = f"{header}\n\n{sub_chunk}" if header else sub_chunk
                all_chunks.append(chunk_with_header)

    return all_chunks

# 5. Process each text file in the content directory
for filename in os.listdir(content_dir):
    if filename.endswith('.md'):
        filepath = os.path.join(content_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

            # Extract Jekyll frontmatter and title
            title = ""
            content = text

            # Check if file has frontmatter (starts with ---)
            if text.startswith('---'):
                # Split on the frontmatter delimiters
                parts = re.split(r'^---\s*$', text, maxsplit=2, flags=re.MULTILINE)
                if len(parts) >= 3:
                    frontmatter_text = parts[1]
                    content = parts[2].strip()

                    # Parse YAML frontmatter
                    try:
                        frontmatter = yaml.safe_load(frontmatter_text)
                        if frontmatter and 'title' in frontmatter:
                            title = frontmatter['title']
                    except yaml.YAMLError:
                        # If YAML parsing fails, continue without title
                        pass

            # 6. Create chunks using header-based splitting with size limits
            print(f"Generating embeddings for {filename}...")
            chunks = create_chunks_from_content(content, MAX_CHUNK_WORDS, OVERLAP_WORDS)

            # 7. Collect chunks with title prefix for embedding
            for chunk in chunks:
                if chunk.strip():
                    all_chunks.append(chunk)
                    if title:
                        all_chunks_with_title.append(f"Title: {title}\n\n{chunk}")
                    else:
                        all_chunks_with_title.append(chunk)

# 8. Encode all chunks with both models
print(f"Encoding {len(all_chunks_with_title)} chunks with all-MiniLM-L6-v2...")
embeddings_minilm = model_minilm.encode(all_chunks_with_title)

print(f"Encoding {len(all_chunks_with_title)} chunks with BAAI/bge-small-en-v1.5...")
embeddings_bge = model_bge.encode(all_chunks_with_title)

# 9. Build document lists
documents_minilm = []
documents_bge = []

for i, chunk in enumerate(all_chunks):
    documents_minilm.append({
        'chunk': chunk,
        'embedding': embeddings_minilm[i].tolist()
    })
    documents_bge.append({
        'chunk': chunk,
        'embedding': embeddings_bge[i].tolist()
    })

# 10. Write both output files
os.makedirs(os.path.dirname(output_file_minilm), exist_ok=True)

with open(output_file_minilm, 'w') as f:
    json.dump(documents_minilm, f, indent=2)
print(f"✅ Successfully created {output_file_minilm} with {len(documents_minilm)} document chunks.")

with open(output_file_bge, 'w') as f:
    json.dump(documents_bge, f, indent=2)
print(f"✅ Successfully created {output_file_bge} with {len(documents_bge)} document chunks.")
