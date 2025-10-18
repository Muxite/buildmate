

# cli 
import os
import subprocess

# gemini
from google import genai

# Initialize the client with your Vertex AI API key
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Choose a Gemini model (use gemini-2.0-pro, gemini-1.5-flash, etc.)
model = "gemini-2.0-flash"


# attempt to compile
# send compilation output to gemini along with "output pure code"
# send fixed code to c 
# compile again
def compile_c_file(c_file: str):
    try:
        result = subprocess.run(
            ["gcc", "-o", "program.out", c_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output = result.stdout + result.stderr
        success = result.returncode == 0
        return success, output.strip()
    except FileNotFoundError:
        return False, "file not found"


# # Send a prompt
# prompt = """

# """
# response = client.models.generate_content(
#     model=model,
#     contents=[{"role": "user", "parts": [{"text": prompt}]}],
# )

# print(response.text)
