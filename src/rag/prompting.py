from typing import Any


SYSTEM_PROMPT = """
You are TechRAG Architect, a grounded technical document assistant.

Your answer MUST be based ONLY on the retrieved context supplied below.

STRICT RULES:

1. Do not use outside knowledge.
2. Do not invent facts, document names, or page numbers.
3. If the retrieved context is insufficient, explicitly say:
   "I don't have enough information in the provided documents to answer this reliably."
4. Every factual paragraph must contain at least one supporting citation.
5. Use ONLY citations from the AVAILABLE VALID CITATIONS list.
6. Copy citations EXACTLY as provided.
7. Never modify a document filename.
8. Never modify or guess a page number.
9. Never cite a source that is not listed in AVAILABLE VALID CITATIONS.
10. Do not mention chunk IDs.
11. Answer clearly and concisely.
"""


def build_valid_citations_list(
    retrieved_chunks: list[dict[str, Any]],
) -> str:
    """
    Build an explicit whitelist of valid citations
    that the LLM can copy exactly.
    """

    citations: list[str] = []

    seen: set[tuple[str, str]] = set()

    for result in retrieved_chunks:
        metadata = (
            result.get(
                "metadata",
                {},
            )
            or {}
        )

        document = str(
            metadata.get(
                "document",
                "",
            )
        ).strip()

        page = str(
            metadata.get(
                "page",
                "",
            )
        ).strip()

        if (
            not document
            or not page
        ):
            continue

        key = (
            document,
            page,
        )

        if key in seen:
            continue

        seen.add(
            key
        )

        citations.append(
            f"[Document: {document}, Page: {page}]"
        )

    if not citations:
        return (
            "No valid citations available."
        )

    return "\n".join(
        f"- {citation}"
        for citation in citations
    )


def build_rag_prompt(
    query: str,
    retrieved_chunks: list[dict[str, Any]],
) -> str:
    """
    Build a strongly grounded RAG prompt from
    retrieved document chunks.
    """

    context_sections: list[str] = []

    for result in retrieved_chunks:
        metadata = (
            result.get(
                "metadata",
                {},
            )
            or {}
        )

        context_sections.append(
            f"""
SOURCE {result['rank']}

Document: {metadata.get('document', 'Unknown document')}
Page: {metadata.get('page', '?')}
Category: {metadata.get('category', 'Unknown')}

CONTENT:
{result.get('text', '')}
""".strip()
        )

    context = (
        "\n\n"
        "----------------------------------------"
        "\n\n"
    ).join(
        context_sections
    )

    valid_citations = (
        build_valid_citations_list(
            retrieved_chunks
        )
    )

    return f"""
{SYSTEM_PROMPT}

USER QUESTION:
{query}

AVAILABLE VALID CITATIONS:
{valid_citations}

RETRIEVED CONTEXT:
{context}

ANSWER REQUIREMENTS:

- Answer only from the retrieved context.
- Include at least one citation.
- Use citations only from AVAILABLE VALID CITATIONS.
- Copy each citation exactly.
- Put citations immediately after the claim they support.
- If several sources support one claim, multiple valid citations may be used.
- Do not create your own citation text.

ANSWER:
""".strip()