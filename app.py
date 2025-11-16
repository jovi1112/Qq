from flask import Flask, request, send_file
import os, subprocess, uuid

app = Flask(__name__)

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    filename = data["filename"]
    code = data["code"]

    job_id = str(uuid.uuid4())
    folder = f"job_{job_id}"
    os.mkdir(folder)

    py_path = os.path.join(folder, filename + ".py")

    # Guardar el código en un archivo
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(code)

    # Ejecutar PyInstaller
    subprocess.run(["pyinstaller", "--onefile", py_path], cwd=folder)

    exe_path = os.path.join(folder, "dist", filename + ".exe")

    return send_file(exe_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
