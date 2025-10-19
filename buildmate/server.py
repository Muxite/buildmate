

from flask import Flask, request, jsonify, send_file
from app.buildmate import BuildMate
import tempfile
import os

app = Flask(__name__)

@app.route("/compile", methods=["POST"])
def compile_c():
    """
    Expects a file upload named 'file' from VS Code extension.
    Saves it temporarily, runs BuildMate.procedure(), 
    returns compiled EXE or error text.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files["file"]

    # Create temp directory for processing
    with tempfile.TemporaryDirectory() as tmpdir:
        src_path = os.path.join(tmpdir, uploaded_file.filename)
        uploaded_file.save(src_path)

        # init
        buildmate = BuildMate(src_path)

        try:
            success, output = buildmate.procedure() # actually run the procedure lol

            exe_path = os.path.splitext(src_path)[0] + ".exe"
            if success and os.path.exists(exe_path):
                # Return the compiled exe
                return send_file(exe_path, as_attachment=True, download_name="program.exe")
            else:
                # Return the compiler output instead
                return jsonify({
                    "success": False,
                    "compiler_output": output
                }), 500

        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
