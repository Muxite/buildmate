import os
import time
import google.generativeai as genai

def call_gemini(
    prompt,
    context=None,
    search_results=None,
    system_instruction=None,
    model="gemini-2.5-flash",
    max_retries=3,
    backoff_factor=2.0
):
    """
    Calls the Gemini LLM endpoint to generate content.

    PARAMETERS:
    - prompt (str): Core instruction or question.
    - context (str, optional): Chat history or problem description.
    - search_results (list or str, optional): External grounding information.
    - system_instruction (str, optional): Instructions to guide the model.
    - model (str): Gemini model to use (default: 'gemini-2.5-flash').
    - max_retries (int): Number of retry attempts for rate limits.
    - backoff_factor (float): Factor for exponential backoff.

    RETURNS:
    - str: The generated text response from Gemini.
    """

    # Initialize the client
    client = genai.Client()

    # Prepare the message list
    messages = []

    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})

    if context:
        messages.append({"role": "user", "content": context})

    if search_results:
        if isinstance(search_results, list):
            search_text = "\n".join(search_results)
        else:
            search_text = str(search_results)
        messages.append({"role": "user", "content": f"Reference data:\n{search_text}"})

    # Add the main prompt last
    messages.append({"role": "user", "content": prompt})

    # Retry logic
    for attempt in range(max_retries):
        try:
            # Call the Gemini model
            response = client.models.generate_content(
                model=model,
                contents=messages
            )
            return response.text
        except Exception as e:
            if attempt == max_retries - 1:
                raise RuntimeError(f"Failed to call Gemini API after {max_retries} attempts: {e}")
            wait_time = backoff_factor ** attempt
            print(f"Error: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

if __name__ == '__main__':
    try:
        result = call_gemini("Hello, Gemini! Please summarize this test.", system_instruction="Act as an expert assistant.")
        print("Gemini response:", result)
    except Exception as e:
        print("Error:", e)
