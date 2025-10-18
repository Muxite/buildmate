import subprocess
import sys
import os

def compile_c_file(c_file):
    if not os.path.exists(c_file):
        print(f"Error: File '{c_file}' does not exist.")
        return

    # Output executable name (remove .c extension)
    exe_file = os.path.splitext(c_file)[0]

    # Run gcc command
    try:
        result = subprocess.run(
            ["gcc", c_file, "-o", exe_file],
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

compile_c_file("app/csrc/hello.c")