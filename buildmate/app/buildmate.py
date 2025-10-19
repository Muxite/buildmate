from app.ai_search import ai_search
from app.call_gemini import GeminiClient
import subprocess
import os


class BuildMate:
    def __init__(self, cfile):
        self.cfile = cfile
        self.gemini_client = GeminiClient()  # Use the GeminiClient for all Gemini-related operations

    def compile_c_file(self):
        if not os.path.exists(self.cfile):
            return False, f"Error: File '{self.cfile}' does not exist."

        exe_file = os.path.splitext(self.cfile)[0] + ".exe"  # name of output exe
        try:
            result = subprocess.run(
                ["x86_64-w64-mingw32-gcc", "-o", exe_file, self.cfile],
                capture_output=True,
                text=True,
            )

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

        return (
            f"Here is the C file:\n{cfile_content}\n\n"
            "Think about what this C file is supposed to do. "
            "Infer what the existing functions and variables are supposed to be.\n"
            "Write what you think each undeclared function/variable should be.\n\n"
            f"Compiler output:\n{compiler_output}\n"
            "YOUR OUTPUT IS PURE C, WRITE INSIDE THE FILE ONLY. NON-C GOES IN COMMENTS."
        )

    def infer_missing_symbols(self, compiler_output):
        prompt = self._make_prompt(compiler_output)

        fixed_code = self.gemini_client.generate(
            prompt=prompt, system_instruction="Focus on fixing and completing the C file."
        )

        with open(self.cfile, "w") as f:
            f.write(fixed_code)

        print(f"Gemini suggestions written to {self.cfile}")
        return fixed_code

    def procedure(self, max_retries=3):
        """
        Try to compile the C file. If compilation fails, try to fix the errors.
        If stuck on the problem, seek online internet help.
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

            self.infer_missing_symbols(output)

        print("All attempts failed. Returning last output.")
        return False, output