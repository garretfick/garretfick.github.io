"""
Retrieval quality evaluation for the ask page RAG pipeline.

For each golden question, this script:
1. Computes the query embedding using the same models as the pipeline.
2. Ranks all chunks by cosine similarity (dot product on normalized vectors).
3. Checks if the top-k retrieved chunks contain the expected content.

Two checks per question:
- Keyword hit: at least one top-k chunk contains at least one expected keyword.
- Title hit: at least one top-k chunk comes from the expected blog post title.

Exit code is non-zero if overall score falls below the threshold.
"""

import json
import sys
import os
import numpy as np
from sentence_transformers import SentenceTransformer

TOP_K = 3
PASS_THRESHOLD = 0.75

MODELS = {
    "all-MiniLM-L6-v2": {
        "model_name": "all-MiniLM-L6-v2",
        "embeddings_file": "_site/static/model/embeddings-all-MiniLM-L6-v2.json",
    },
    "bge-small-en-v1.5": {
        "model_name": "BAAI/bge-small-en-v1.5",
        "embeddings_file": "_site/static/model/embeddings-bge-small-en-v1.5.json",
    },
}


def load_embeddings(filepath):
    with open(filepath, "r") as f:
        docs = json.load(f)
    chunks = [d["chunk"] for d in docs]
    embeddings = np.array([d["embedding"] for d in docs])
    return chunks, embeddings


def retrieve_top_k(query_embedding, embeddings, chunks, k):
    """Return top-k chunks by cosine similarity (dot product on L2-normalized vectors)."""
    similarities = embeddings @ query_embedding
    top_indices = np.argsort(similarities)[::-1][:k]
    return [(chunks[i], float(similarities[i])) for i in top_indices]


def check_keyword_hit(retrieved_chunks, expected_keywords):
    """True if at least one chunk contains at least one expected keyword (case-insensitive)."""
    for chunk, _ in retrieved_chunks:
        chunk_lower = chunk.lower()
        for keyword in expected_keywords:
            if keyword.lower() in chunk_lower:
                return True
    return False


def check_title_hit(retrieved_chunks, expected_title):
    """True if at least one chunk contains text from the expected post title."""
    title_lower = expected_title.lower()
    for chunk, _ in retrieved_chunks:
        if title_lower in chunk.lower():
            return True
    # Also check for the "Title: ..." prefix used in embeddings generation.
    for chunk, _ in retrieved_chunks:
        if f"title: {title_lower}" in chunk.lower():
            return True
    return False


def evaluate_model(model_key, model_config, golden_questions):
    print(f"\n{'='*60}")
    print(f"Evaluating model: {model_key}")
    print(f"{'='*60}")

    embeddings_path = model_config["embeddings_file"]
    if not os.path.exists(embeddings_path):
        print(f"  ERROR: embeddings file not found: {embeddings_path}")
        return None

    chunks, embeddings = load_embeddings(embeddings_path)
    # Normalize embeddings for dot-product similarity.
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1
    embeddings = embeddings / norms

    print(f"  Loaded {len(chunks)} chunks")

    model = SentenceTransformer(model_config["model_name"])

    keyword_hits = 0
    title_hits = 0
    total = len(golden_questions)

    for q in golden_questions:
        query = q["question"]
        query_embedding = model.encode(query)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)

        retrieved = retrieve_top_k(query_embedding, embeddings, chunks, TOP_K)

        kw_hit = check_keyword_hit(retrieved, q["expected_keywords"])
        tt_hit = check_title_hit(retrieved, q["expected_title"])

        keyword_hits += int(kw_hit)
        title_hits += int(tt_hit)

        status = "PASS" if (kw_hit and tt_hit) else "FAIL"
        print(f"  [{status}] {query}")
        if not kw_hit:
            print(f"         keyword miss (expected: {q['expected_keywords']})")
        if not tt_hit:
            print(f"         title miss (expected: {q['expected_title']})")
        if status == "FAIL":
            print(f"         top chunk: {retrieved[0][0][:100]}...")

    keyword_score = keyword_hits / total
    title_score = title_hits / total
    combined_score = (keyword_score + title_score) / 2

    print(f"\n  Results for {model_key}:")
    print(f"    Keyword hit rate: {keyword_hits}/{total} ({keyword_score:.0%})")
    print(f"    Title hit rate:   {title_hits}/{total} ({title_score:.0%})")
    print(f"    Combined score:   {combined_score:.0%}")

    return combined_score


def main():
    golden_path = os.path.join(os.path.dirname(__file__), "golden_retrieval.json")
    with open(golden_path, "r") as f:
        golden_questions = json.load(f)

    print(f"Loaded {len(golden_questions)} golden questions")

    all_passed = True
    for model_key, model_config in MODELS.items():
        score = evaluate_model(model_key, model_config, golden_questions)
        if score is None:
            print(f"\n  SKIP: {model_key} (embeddings not available)")
            continue
        if score < PASS_THRESHOLD:
            print(f"\n  FAIL: {model_key} score {score:.0%} < threshold {PASS_THRESHOLD:.0%}")
            all_passed = False
        else:
            print(f"\n  PASS: {model_key} score {score:.0%} >= threshold {PASS_THRESHOLD:.0%}")

    print(f"\n{'='*60}")
    if all_passed:
        print("Overall: PASS")
    else:
        print("Overall: FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
