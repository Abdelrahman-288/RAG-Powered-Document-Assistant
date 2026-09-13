from typing import Any


SYSTEM_PROMPT = """
You are TechRAG Architect, a technical assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not invent facts that are not supported by the context.
2. If the context does not contain enough information, say that you do not
   have enough information in the provided documents.
3. Explain the answer clearly and accurately.
4. Cite the supporting sources using the format:
   [Document: <document name>, Page: <page number>]
5. Do not mention chunk IDs to the user.
"""


def build_rag_prompt(
    query: str,
    retrieved_chunks: list[dict[str, Any]],
) -> str:
    """
    Build a grounded RAG prompt from retrieved document chunks.
    """

    context_sections: list[str] = []

    for result in retrieved_chunks:
        metadata = result["metadata"]

        context_sections.append(
            f"""
SOURCE {result['rank']}
Document: {metadata['document']}
Page: {metadata['page']}
Category: {metadata['category']}

{result['text']}
""".strip()
        )

    context = "\n\n---\n\n".join(context_sections)

    return f"""
{SYSTEM_PROMPT}

USER QUESTION:
{query}

CONTEXT:
{context}

ANSWER:
""".strip()