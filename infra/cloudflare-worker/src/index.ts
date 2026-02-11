/**
 * Cloudflare Worker for RAG-based question answering
 *
 * Endpoints:
 * - POST /ask: Full RAG pipeline - embedding, retrieval, generation
 * - GET /health: Health check
 */

export interface Env {
  AI: Ai;
  EMBEDDINGS_KV: KVNamespace;
}

interface AskRequest {
  question: string;
}

interface EmbeddingDoc {
  chunk: string;
  embedding: number[];
}

const ALLOWED_ORIGINS = [
  "https://garretfick.com",
  "https://www.garretfick.com",
  "https://garretfick.github.io",
  "http://localhost:4000",
];

/**
 * Cosine similarity via dot product (vectors are L2-normalized).
 */
function dotProduct(a: number[], b: number[]): number {
  let sum = 0;
  for (let i = 0; i < a.length; i++) {
    sum += a[i] * b[i];
  }
  return sum;
}

function getCORSHeaders(request: Request): Record<string, string> {
  const origin = request.headers.get("Origin") || "";
  const headers: Record<string, string> = {
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
  };
  if (ALLOWED_ORIGINS.includes(origin)) {
    headers["Access-Control-Allow-Origin"] = origin;
  }
  return headers;
}

function jsonResponse(
  body: unknown,
  status: number,
  request: Request,
): Response {
  const corsHeaders = getCORSHeaders(request);
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...corsHeaders },
  });
}

/**
 * POST /ask - Full RAG pipeline
 *
 * 1. Validate question
 * 2. Compute query embedding with bge-small-en-v1.5
 * 3. Load pre-computed embeddings from KV
 * 4. Cosine similarity search, take top 3
 * 5. Generate answer with Llama 3.1 8B Instruct
 */
async function handleAsk(request: Request, env: Env): Promise<Response> {
  let body: AskRequest;
  try {
    body = await request.json() as AskRequest;
  } catch {
    return jsonResponse({ error: "Invalid JSON body" }, 400, request);
  }

  const { question } = body;
  if (!question || typeof question !== "string" || question.trim().length === 0) {
    return jsonResponse({ error: "Missing or empty question" }, 400, request);
  }
  if (question.length > 500) {
    return jsonResponse({ error: "Question must be 500 characters or fewer" }, 400, request);
  }

  // Compute query embedding
  const embeddingResponse = await env.AI.run("@cf/baai/bge-small-en-v1.5", {
    text: [question],
  });
  const queryEmbedding = (embeddingResponse as { data: number[][] }).data[0];

  // Load pre-computed embeddings from KV
  const docs = await env.EMBEDDINGS_KV.get<EmbeddingDoc[]>("embeddings", { type: "json" });
  if (!docs) {
    return jsonResponse({ error: "Embeddings not found" }, 500, request);
  }

  // Rank by cosine similarity (dot product since vectors are normalized)
  const ranked = docs
    .map((doc) => ({ chunk: doc.chunk, similarity: dotProduct(queryEmbedding, doc.embedding) }))
    .sort((a, b) => b.similarity - a.similarity);

  const topChunks = ranked.slice(0, 3);
  const context = topChunks.map((c) => c.chunk).join("\n\n---\n\n");

  // Generate answer
  const aiResponse = await env.AI.run("@cf/meta/llama-3.1-8b-instruct", {
    messages: [
      {
        role: "system",
        content:
          "You are a helpful assistant that answers questions about Garret Fick's blog. Answer based ONLY on the provided context. If the context doesn't contain enough information, say so.",
      },
      {
        role: "user",
        content: `Context:\n${context}\n\nQuestion: ${question}`,
      },
    ],
    max_tokens: 512,
  });

  return jsonResponse(
    {
      answer: (aiResponse as { response: string }).response,
      sources: topChunks.map((c) => c.chunk),
    },
    200,
    request,
  );
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: getCORSHeaders(request) });
    }

    const url = new URL(request.url);

    try {
      if (url.pathname === "/ask" && request.method === "POST") {
        return await handleAsk(request, env);
      }

      if (url.pathname === "/health" && request.method === "GET") {
        return jsonResponse({ status: "ok" }, 200, request);
      }

      if (request.method !== "GET" && request.method !== "POST") {
        return jsonResponse({ error: "Method Not Allowed" }, 405, request);
      }

      return jsonResponse({ error: "Not Found" }, 404, request);
    } catch (error) {
      console.error("Worker error:", error);
      return jsonResponse({ error: "Internal Server Error" }, 500, request);
    }
  },
};
