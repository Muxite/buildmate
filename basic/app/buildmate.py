

import subprocess
import sys
import os

from google import genai


# C_FILE = "csrc/hello.c"
MODEL = "gemini-2.0-flash"

class buildmate:

    cfile = ""
    api_key = os.getenv("GOOGLE_API_KEY")
    


    def __init__(self, cfile, api_key):
        
        if not api_key:
            raise RuntimeError("Missing GOOGLE_API_KEY environment variable.")
        self.cfile = cfile
        self.api_key = api_key
        

    def compile_c_file(self):
        c_file = self.cfile
        if not os.path.exists(c_file):
            print(f"Error: File '{c_file}' does not exist.")
            return

        exe_file = os.path.splitext(c_file)[0]

        try:
            result = subprocess.run(
                ["gcc", "-o", exe_file, c_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"Compilation successful! Executable: {exe_file}")
            else:
                print("Compilation failed with errors:")
                print(result.stderr)
        except Exception as e:
            print(f"Error running gcc: {e}")


    def infer_missing_symbols(self, output: str):
       
        client = genai.Client(api_key=self.api_key)
        
        cfileout = "" 
        with open(self.cfile, "r") as f:
            cfileout = f.read()


        prompt = (
            f"Here is the C file: {cfileout}\n"
            "Think about what this C file is supposed to do. Infer what the existing functions and variables are supposed to be.\n"
            "Write what you think each undeclared function/variable should be"
            f"Compiler output:\n{output}"
            "YOUR OUTPUT IS PURE C, YOU ARE WRITING INSIDE THE FILE. ONLY WRITE NON-C IN COMMENTS"
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
        )

        lines = response.text.splitlines()
        lines = lines[1:-1]
        cleanstr = "\n".join(lines)
        with open(self.cfile, "w") as f:
            f.write(cleanstr)
        
        return response.text
    
    def procedure(self):
        text1 = self.compile_c_file()
        self.infer_missing_symbols(text1)
        text2= self.compile_c_file()
        self.infer_missing_symbols(text2)
        return self.compile_c_file()
