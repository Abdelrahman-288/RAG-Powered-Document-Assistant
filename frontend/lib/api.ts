const API_BASE_URL = "http://127.0.0.1:8000";

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
};

export async function askQuestion(
  question: string,
  category: string | null
): Promise<QueryResponse> {
  const response = await fetch(
    "http://127.0.0.1:8000/query",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
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