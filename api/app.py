import eventlet

eventlet.monkey_patch()

import random
import os
import subprocess
import logging
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_socketio import SocketIO
import shutil

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

UPLOAD_FOLDER = "/tmp/uploads"
DECOMPILE_FOLDER = "/tmp/decompiled"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECOMPILE_FOLDER, exist_ok=True)


@app.route("/", methods=["GET"])
def ping():
    return jsonify({"error": "pong"}), 200


# def run_jsluice(decompiled_path):
#     for root, dirs, files in os.walk(decompiled_path):
#         for file in files:
#             if file.endswith('.js'):
#                 file_path = os.path.join(root, file)
#                 with open(file_path, 'r') as f:
#                     content = f.read()
#                     results = jsluice.digest_js(content)
#                     for endpoint in results['endpoints']:
#                         url = endpoint['url']
#                         method = endpoint.get('method', 'UNKNOWN')
#                         add_endpoint(current_project_id, url, method, 'jsluice')
#                         socketio.emit('new_endpoint', {'url': url, 'method': method, 'source': 'jsluice'})


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        socketio.start_background_task(decompile_apk, filepath)
        return jsonify({"message": "File uploaded and decompilation started"}), 200


def decompile_apk(filepath):
    output_dir = os.path.join(
        DECOMPILE_FOLDER, os.path.splitext(os.path.basename(filepath))[0]
    )

    def run_decompilation():
        try:
            process = subprocess.Popen(
                ["jadx", "-v", "-d", output_dir, filepath],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )

            for line in process.stdout:
                print(line, end="")  # Print to server console
                socketio.emit("console_output", {"data": line.strip()}, namespace="/")

            process.wait()

            if process.returncode == 0:
                socketio.emit(
                    "decompile_complete", {"status": "success"}, namespace="/"
                )
            else:
                socketio.emit("decompile_complete", {"status": "error"}, namespace="/")

        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            logging.error(error_msg)
            socketio.emit("console_output", {"data": error_msg}, namespace="/")
            socketio.emit("decompile_complete", {"status": "error"}, namespace="/")

    socketio.start_background_task(run_decompilation)


@app.route("/files", methods=["GET"])
def list_files():
    files = []
    for root, dirs, filenames in os.walk(DECOMPILE_FOLDER):
        for filename in filenames:
            relative_path = os.path.relpath(
                os.path.join(root, filename), DECOMPILE_FOLDER
            )
            files.append(relative_path)
    return jsonify({"files": files})


@app.route("/wipe", methods=["DELETE"])
def wipe_files():
    folders = []
    for item in os.listdir(DECOMPILE_FOLDER):
        item_path = os.path.join(DECOMPILE_FOLDER, item)
        if os.path.isdir(item_path):
            folders.append(item)
            shutil.rmtree(item_path)
        elif os.path.isfile(item_path):
            os.remove(item_path)

    return jsonify({"message": "Decompiled files wiped", "folders": folders})


@app.route("/file/<path:filepath>", methods=["GET"])
def get_file(filepath):
    full_path = os.path.join(DECOMPILE_FOLDER, filepath)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return send_file(full_path)
    else:
        return jsonify({"error": "File not found", "path": full_path}), 404


def emit_random_message():
    prefixes = ["ERROR - ", "WARN - ", "INFO - ", "DEBUG - ", "SUCCESS - ", ""]
    messages = [
        "Something went wrong!",
        "Resource not found!",
        "Unexpected condition!",
        "Check configurations!",
        "Critical error encountered!",
    ]

    while True:
        prefix = random.choice(prefixes)
        message = random.choice(messages)
        socketio.emit("console_output", {"data": prefix + message}, namespace="/")
        eventlet.sleep(1)


if __name__ == "__main__":
    print("🚀 Starting APK Decompiler Backend")
    # socketio.start_background_task(emit_random_message)
    socketio.run(
        app,
        host="0.0.0.0",
        port=os.getenv("PORT", 5000),
        debug=True,
        use_reloader=False,
        log_output=False,
    )
