from ollama import Client


DEFAULT_MODEL = "gemma3:4b"


class GenerationService:
    """
    Thin wrapper around the local Ollama generation API.
    """

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        host: str = "http://localhost:11434",
    ) -> None:
        self.model_name = model_name
        self.client = Client(host=host)

    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
    ) -> str:
        """
        Generate a response from the local Ollama model.
        """

        response = self.client.generate(
            model=self.model_name,
            prompt=prompt,
            options={
                "temperature": temperature,
            },
        )

        return response["response"].strip()