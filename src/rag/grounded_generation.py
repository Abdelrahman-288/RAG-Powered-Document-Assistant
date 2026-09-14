from typing import Any

from src.rag.citation_validator import validate_citations
from src.rag.generation import GenerationService
from src.rag.prompting import build_rag_prompt


class GroundedGenerationService:
    """
    Generates grounded RAG answers and validates citations.

    If the first answer contains invalid citations, the system
    retries once using stricter citation instructions.
    """

    def __init__(
        self,
        generation_service: GenerationService,
        max_retries: int = 1,
    ) -> None:
        self.generation_service = generation_service
        self.max_retries = max_retries

    def _build_retry_prompt(
        self,
        query: str,
        retrieved_chunks: list[dict[str, Any]],
        previous_answer: str,
        invalid_citations: list[tuple[str, int]],
    ) -> str:
        """
        Build a stricter prompt when the first answer
        contains unsupported citations.
        """

        base_prompt = build_rag_prompt(
            query=query,
            retrieved_chunks=retrieved_chunks,
        )

        invalid_text = "\n".join(
            f"- {document}, Page {page}"
            for document, page in invalid_citations
        )

        retry_instructions = f"""

IMPORTANT CITATION CORRECTION:

Your previous answer contained unsupported citations.

Invalid citations:
{invalid_text}

Previous answer:
{previous_answer}

Rewrite the answer.

STRICT RULES:
1. Use ONLY the provided retrieved context.
2. Cite ONLY document/page combinations that appear in the context.
3. Do NOT invent page numbers.
4. Do NOT cite a document unless that exact document appears in the context.
5. Every factual claim that depends on the retrieved context should use:
   [Document: <document name>, Page: <page number>]
6. If the available context is insufficient, explicitly say so.
7. Do not mention these correction instructions.
"""

        return base_prompt + retry_instructions

    def generate_grounded_answer(
        self,
        query: str,
        retrieved_chunks: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Generate an answer and ensure citations are grounded.

        Returns:
            {
                "answer": str,
                "validation": dict,
                "attempts": int,
                "success": bool
            }
        """

        prompt = build_rag_prompt(
            query=query,
            retrieved_chunks=retrieved_chunks,
        )

        answer = self.generation_service.generate(
            prompt
        )

        validation = validate_citations(
            answer=answer,
            retrieved_chunks=retrieved_chunks,
        )

        attempts = 1

        if validation["all_valid"]:
            return {
                "answer": answer,
                "validation": validation,
                "attempts": attempts,
                "success": True,
            }

        for _ in range(self.max_retries):
            retry_prompt = self._build_retry_prompt(
                query=query,
                retrieved_chunks=retrieved_chunks,
                previous_answer=answer,
                invalid_citations=validation["invalid"],
            )

            answer = self.generation_service.generate(
                retry_prompt,
                temperature=0.1,
            )

            validation = validate_citations(
                answer=answer,
                retrieved_chunks=retrieved_chunks,
            )

            attempts += 1

            if validation["all_valid"]:
                return {
                    "answer": answer,
                    "validation": validation,
                    "attempts": attempts,
                    "success": True,
                }

        fallback_answer = (
            "I found relevant information, but I could not produce "
            "an answer with fully validated citations. Please inspect "
            "the retrieved sources directly."
        )

        return {
            "answer": fallback_answer,
            "validation": validation,
            "attempts": attempts,
            "success": False,
        }
    