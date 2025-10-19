from app.ai_search import ai_search
import subprocess
import os
from google import genai


class BuildMate:
    def __init__(self, cfile):
        self.cfile = cfile
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        if not self.api_key:
            raise RuntimeError("Missing GOOGLE_API_KEY environment variable.")

    def compile_c_file(self):
        if not os.path.exists(self.cfile):
            return False, f"Error: File '{self.cfile}' does not exist."

        exe_file = os.path.splitext(self.cfile)[0] + ".exe"  # name of output exe
        try:
            result = subprocess.run(["x86_64-w64-mingw32-gcc", "-o", exe_file, self.cfile], capture_output=True, text=True)

            output = result.stdout + result.stderr
            success = result.returncode == 0

            if success:
                print(f"Compilation successful! Executable: {exe_file}")
            else:
                print("Compilation failed with errors:")
                print(result.stderr)

            return success, output

        except Exception as e:
            return False, f"Error running gcc: {e}"

    def _make_prompt(self, compiler_output):
        with open(self.cfile, "r") as f:
            cfile_content = f.read()

        prompt = (
            f"Here is the C file:\n{cfile_content}\n\n"
            "Think about what this C file is supposed to do. "
            "Infer what the existing functions and variables are supposed to be.\n"
            "Write what you think each undeclared function/variable should be.\n"
            "You should write as full coverage as you can (implement every function), don't leave methods or variables blank. The user is trusting you to provide code that will compile and give some output that is congruent with expected specification.\n"
            f"Compiler output:\n{compiler_output}\n"
            "YOU ARE NOT ALLOWED TO INCLUDE ANY LIBRARIES. NOT EVEN STD."
            "YOUR OUTPUT IS PURE C, WRITE INSIDE THE FILE ONLY. NO COMMENTS (nobody will read this code)"
        )

        return prompt

    def infer_missing_symbols(self, compiler_output):

        prompt = self._make_prompt(compiler_output)

        response = self.client.models.generate_content(
            model=self.model,
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
        )

        # Remove first and last line
        lines = response.text.splitlines()
        if len(lines) >= 3:
            clean_lines = lines[1:-1]
        else:
            clean_lines = lines
        fixed_code = "\n".join(clean_lines)

        # Overwrite C file
        with open(self.cfile, "w") as f:
            f.write(fixed_code)

        print(f"Gemini suggestions written to {self.cfile}")
        return fixed_code

    def procedure(self, max_retries=3):
        """
        Full workflow: compile → send to Gemini if errors → recompile
        """
        for attempt in range(max_retries + 1):
            success, output = self.compile_c_file()
            if success:
                return True, output

            print(f"Attempt {attempt + 1} failed.")

            # Only seek online AI help after the first failed attempt, appends extra details
            if attempt >= -1:
                prompt = self._make_prompt(output)
                output += ai_search(prompt)

            # Always try to infer missing symbols, with our without extra details.
            self.infer_missing_symbols(output)


            # If we reach here, all retries failed
        print("All attempts failed. Returning last output.")
        return False, output
