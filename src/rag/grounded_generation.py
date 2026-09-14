from typing import Any

from src.rag.citation_validator import (
    validate_citations,
)
from src.rag.generation import (
    GenerationService,
)
from src.rag.prompting import (
    build_rag_prompt,
    build_valid_citations_list,
)


class GroundedGenerationService:
    """
    Generate grounded RAG answers and validate
    all citations against retrieved sources.
    """

    def __init__(
        self,
        generation_service: GenerationService,
        max_retries: int = 1,
    ) -> None:

        self.generation_service = (
            generation_service
        )

        self.max_retries = (
            max_retries
        )


    def _build_retry_prompt(
        self,
        query: str,
        retrieved_chunks: list[
            dict[
                str,
                Any,
            ]
        ],
        previous_answer: str,
        validation: dict[
            str,
            Any,
        ],
    ) -> str:
        """
        Build a stricter correction prompt for:
        - invalid citations
        - missing citations
        """

        base_prompt = (
            build_rag_prompt(
                query=query,
                retrieved_chunks=(
                    retrieved_chunks
                ),
            )
        )


        valid_citations = (
            build_valid_citations_list(
                retrieved_chunks
            )
        )


        invalid_citations = (
            validation.get(
                "invalid",
                [],
            )
            or []
        )


        if invalid_citations:

            invalid_text = "\n".join(
                (
                    f"- [Document: "
                    f"{document}, "
                    f"Page: {page}]"
                )

                for (
                    document,
                    page,
                )

                in invalid_citations
            )

        else:

            invalid_text = (
                "The previous answer contained "
                "no valid citations."
            )


        retry_instructions = f"""

CITATION CORRECTION REQUIRED

The previous answer failed citation validation.

PROBLEM:
{invalid_text}

PREVIOUS ANSWER:
{previous_answer}

ONLY THE FOLLOWING CITATIONS ARE VALID:

{valid_citations}

Rewrite the answer from scratch.

STRICT RULES:

1. Use ONLY the retrieved context.
2. Include at least one citation.
3. Use ONLY citations listed above.
4. Copy every citation EXACTLY.
5. Do not change document filenames.
6. Do not change page numbers.
7. Do not invent citations.
8. Put citations directly after the claims they support.
9. If the retrieved context is insufficient, say so.
10. Do not mention these correction instructions.

CORRECTED ANSWER:
"""


        return (
            base_prompt
            + retry_instructions
        )


    def generate_grounded_answer(
        self,
        query: str,
        retrieved_chunks: list[
            dict[
                str,
                Any,
            ]
        ],
    ) -> dict[str, Any]:
        """
        Generate a grounded answer and validate
        its citations.
        """

        prompt = (
            build_rag_prompt(
                query=query,
                retrieved_chunks=(
                    retrieved_chunks
                ),
            )
        )


        # --------------------------------------------------
        # First generation attempt
        # --------------------------------------------------
        answer = (
            self
            .generation_service
            .generate(
                prompt,
                temperature=0.1,
            )
        )


        validation = (
            validate_citations(
                answer=answer,
                retrieved_chunks=(
                    retrieved_chunks
                ),
            )
        )


        attempts = 1


        # --------------------------------------------------
        # Successful first attempt
        # --------------------------------------------------
        if (
            validation[
                "all_valid"
            ]
        ):

            return {
                "answer":
                    answer,

                "validation":
                    validation,

                "attempts":
                    attempts,

                "success":
                    True,
            }


        # --------------------------------------------------
        # Retry missing/invalid citations
        # --------------------------------------------------
        for _ in range(
            self.max_retries
        ):

            retry_prompt = (
                self._build_retry_prompt(
                    query=query,

                    retrieved_chunks=(
                        retrieved_chunks
                    ),

                    previous_answer=(
                        answer
                    ),

                    validation=(
                        validation
                    ),
                )
            )


            answer = (
                self
                .generation_service
                .generate(
                    retry_prompt,
                    temperature=0.0,
                )
            )


            validation = (
                validate_citations(
                    answer=answer,

                    retrieved_chunks=(
                        retrieved_chunks
                    ),
                )
            )


            attempts += 1


            if (
                validation[
                    "all_valid"
                ]
            ):

                return {
                    "answer":
                        answer,

                    "validation":
                        validation,

                    "attempts":
                        attempts,

                    "success":
                        True,
                }


        # --------------------------------------------------
        # Safe fallback after retries fail
        # --------------------------------------------------
        fallback_answer = (
            "I found relevant information in the "
            "retrieved documents, but I could not "
            "produce an answer with fully validated "
            "citations. Please inspect the retrieved "
            "sources directly."
        )


        return {
            "answer":
                fallback_answer,

            "validation":
                validation,

            "attempts":
                attempts,

            "success":
                False,
        }