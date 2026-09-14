const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://127.0.0.1:8000";


export type SourceItem = {
  rank: number;
  document: string;
  page: number | string;
  category: string;
  similarity: number;
  reranker_score: number | null;
};


export type QueryResponse = {
  question: string;
  answer: string;

  sources: SourceItem[];

  citation_valid: boolean;
  citation_count: number;
  invalid_citations: string[];

  generation_attempts: number;
  grounding_success: boolean;

  needs_category_selection: boolean;
  suggested_categories: string[];

  /*
   * The actual category used by the backend.
   *
   * Example:
   * User selects Auto.
   * Backend determines "cybersecurity".
   *
   * category selected by user = Auto
   * resolved_category = cybersecurity
   */
  resolved_category: string | null;
};


export type StatsResponse = {
  indexed_chunks: number;

  categories: string[];

  embedding_model: string;

  generation_model: string;

  reranker_enabled: boolean;

  reranker_model: string | null;
};


export type KnowledgeBaseDocument = {
  document: string;

  category: string;

  chunk_count: number;
};


export type KnowledgeBaseCategory = {
  category: string;

  document_count: number;

  chunk_count: number;

  documents: KnowledgeBaseDocument[];
};


export type KnowledgeBaseResponse = {
  total_chunks: number;

  total_documents: number;

  total_categories: number;

  categories: KnowledgeBaseCategory[];
};


/**
 * Ask the RAG backend a question.
 *
 * category:
 * - null = Auto routing
 * - string = manually selected field
 */
export async function askQuestion(
  question: string,
  category: string | null
): Promise<QueryResponse> {
  const response = await fetch(
    `${API_BASE_URL}/query`,
    {
      method: "POST",

      headers: {
        "Content-Type":
          "application/json",
      },

      body: JSON.stringify({
        question,
        category,
      }),
    }
  );


  if (!response.ok) {
    const errorText =
      await response.text();

    throw new Error(
      `Backend error ${response.status}: ${errorText}`
    );
  }


  return response.json();
}


/**
 * Get vector-store and model statistics.
 */
export async function getStats():
  Promise<StatsResponse> {
  const response = await fetch(
    `${API_BASE_URL}/stats`
  );


  if (!response.ok) {
    const errorText =
      await response.text();

    throw new Error(
      `Backend error ${response.status}: ${errorText}`
    );
  }


  return response.json();
}


/**
 * Get the complete indexed knowledge-base
 * overview grouped by category/document.
 */
export async function getKnowledgeBase():
  Promise<KnowledgeBaseResponse> {
  const response = await fetch(
    `${API_BASE_URL}/knowledge-base`
  );


  if (!response.ok) {
    const errorText =
      await response.text();

    throw new Error(
      `Backend error ${response.status}: ${errorText}`
    );
  }


  return response.json();
}