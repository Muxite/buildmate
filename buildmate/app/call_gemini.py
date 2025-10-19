import os
import time
from google import genai

class GeminiClient:
    """
    Wrapper for interacting with Google Gemini / GenAI models.
    Handles retries, system instructions, context, and optional reference data.
    """

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    def generate(
        self,
        prompt: str,
        context: str = None,
        reference: str | list[str] = None,
        system_instruction: str = None,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
    ) -> str:
        """
        Sends a prompt to the Gemini model and returns the generated text.
        Retries on failure with exponential backoff.

        Args:
            prompt (str): Main user prompt.
            context (str, optional): Previous chat or problem description.
            reference (str | list[str], optional): Supporting reference info.
            system_instruction (str, optional): Instructions for model behavior.
            max_retries (int): Max retry attempts on failure.
            backoff_factor (float): Exponential backoff factor for retries.

        Returns:
            str: Generated response from the model.
        """
        messages = []

        full_prompt = ""

        if system_instruction:
            full_prompt += f"System instruction:\n{system_instruction}\n\n"
        if context:
            full_prompt += f"Context:\n{context}\n\n"
        if reference:
            ref_text = "\n".join(reference) if isinstance(reference, list) else str(reference)
            full_prompt += f"Reference data:\n{ref_text}\n\n"

        full_prompt += f"User prompt:\n{prompt}"

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=full_prompt
                )
                return response.text
            except Exception as e:
                if attempt == max_retries - 1:
                    raise RuntimeError(f"Failed to call Gemini after {max_retries} attempts: {e}")
                wait_time = backoff_factor ** attempt
                print(f"Error calling Gemini: {e}. Retrying in {wait_time:.1f} sec...")
                time.sleep(wait_time)


if __name__ == "__main__":
    try:
        gemini = GeminiClient(model="gemini-2.5-flash")
        result = gemini.generate(
            "Hello, Gemini! Please summarize this test.",
            system_instruction="Act as an expert assistant."
        )
        print("Gemini response:\n", result)
    except Exception as e:
        print("Error:", e)
