from typing import Any

import ollama


DEFAULT_MODEL = "gemma3:4b"


class GenerationService:
    """
    Handles text generation using a local Ollama model.
    """

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
    ) -> None:

        self.model_name = (
            model_name
        )


    def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
    ) -> str:
        """
        Generate a response from the configured
        Ollama model.

        Parameters
        ----------
        prompt:
            Complete prompt passed to the LLM.

        temperature:
            Sampling temperature.
            Lower values make generation more
            deterministic.

        Returns
        -------
        str
            Generated text.
        """

        if not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )


        try:
            response: Any = (
                ollama.generate(
                    model=self.model_name,
                    prompt=prompt,
                    options={
                        "temperature":
                            temperature,
                    },
                )
            )

        except Exception as exc:
            raise RuntimeError(
                f"Ollama generation failed "
                f"for model "
                f"'{self.model_name}': "
                f"{exc}"
            ) from exc


        # --------------------------------------------------
        # Newer Ollama Python clients may return an object
        # with a .response attribute.
        # --------------------------------------------------
        if hasattr(
            response,
            "response",
        ):
            generated_text = (
                response.response
            )

        # --------------------------------------------------
        # Older/alternative clients may return a dictionary.
        # --------------------------------------------------
        elif isinstance(
            response,
            dict,
        ):
            generated_text = (
                response.get(
                    "response",
                    "",
                )
            )

        else:
            generated_text = str(
                response
            )


        generated_text = (
            str(
                generated_text
            )
            .strip()
        )


        if not generated_text:
            raise RuntimeError(
                "Ollama returned an empty response."
            )


        return generated_text