import eventlet
from sqlalchemy.util import constructor_key

eventlet.monkey_patch()

import re
import os
import subprocess
import logging
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_socketio import SocketIO
import shutil
from database import (
    add_project,
    add_endpoint,
    add_firebase_key,
    get_project_endpoints,
    get_project_firebase_keys,
)

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

UPLOAD_FOLDER = "/tmp/uploads"
DECOMPILE_FOLDER = "/tmp/decompiled"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECOMPILE_FOLDER, exist_ok=True)


# Analysis functions
def run_url_regex_scan(decompiled_path, project_id):
    print(f"Running URL regex scan on {decompiled_path}")
    console_output("Starting URL regex scan...", type="info")
    url_pattern = re.compile(
        r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*(?:\?\S+)?"
    )

    for root, _, files in os.walk(decompiled_path):
        for file in files:
            file_path = os.path.join(root, file)

            console_output(f"Scanning file: {file_path}", type="debug")

            try:
                with open(file_path, "r", errors="ignore") as f:
                    content = f.read()
                    urls = url_pattern.findall(content)
                    for url in urls:
                        add_endpoint(project_id, url, "UNKNOWN", "regex")
                        console_output(f"Regex sweep found URL: {url}")

            except Exception as e:
                console_output(f"Error processing file {file_path}: {e}", type="error")

    console_output("URL regex scan complete.", type="info")


def run_firebase_scan(decompiled_path, project_id):
    print(f"Running Firebase scan on {decompiled_path}")
    console_output("Starting Firebase scan...", type="info")
    firebase_pattern = re.compile(r"AIzaSy[0-9A-Za-z_-]{33}")

    found_count = 0

    for root, _, files in os.walk(decompiled_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", errors="ignore") as f:
                    content = f.read()
                    firebase_keys = firebase_pattern.findall(content)
                    for key in firebase_keys:
                        found_count += 1
                        add_firebase_key(project_id, key)
                        console_output(f"Firebase key found: {key}")
            except Exception as e:
                console_output(f"Error processing file {file_path}: {e}", type="error")

    console_output(f"Firebase scan complete, found keys: {found_count}", type="info")


def run_analysis(decompiled_path, project_id, analyzers=None):
    print(f"Running analysis on {decompiled_path}")
    console_output("Starting analysis...", type="info")

    if analyzers is None or len(analyzers) == 0:
        analyzers = ["regex", "firebase"]

    console_output("Using analyzers: {analyzers}", type="info")

    for analyzer in analyzers:

        if analyzer == "regex":
            run_url_regex_scan(decompiled_path, project_id)
        elif analyzer == "firebase":
            run_firebase_scan(decompiled_path, project_id)
        else:
            console_output(f"Unknown analyzer: {analyzer}", type="error")


# API Endpoints
@app.route("/", methods=["GET"])
def ping():
    console_output("Ping request received", type="info")
    return jsonify({"error": "pong"}), 200


@app.route("/upload", methods=["POST"])
def upload_file():
    console_output("Upload request received", type="info")

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        analyzers = request.form.getlist("analyzers")
        socketio.start_background_task(decompile_and_analyze, filepath, analyzers)
        return (
            jsonify({"message": "File uploaded, decompilation and analysis started"}),
            200,
        )


def decompile_and_analyze(filepath, analyzers):
    output_dir = os.path.join(
        DECOMPILE_FOLDER, os.path.splitext(os.path.basename(filepath))[0]
    )

    def run_decompilation_and_analysis():
        try:
            process = subprocess.Popen(
                ["jadx", "-d", output_dir, filepath],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )

            for line in process.stdout:
                print(line, end="")
                console_output(line.strip())

            process.wait()

            if process.returncode == 0:
                socketio.emit(
                    "decompile_complete", {"status": "success"}, namespace="/"
                )

                # Create a new project in the database
                project_id = add_project(
                    f"Analysis_{os.path.basename(filepath)}",
                    os.path.splitext(os.path.basename(filepath))[0],
                )

                socketio.emit(
                    "project_created", {"project_id": project_id}, namespace="/"
                )

                # Run analysis
                console_output(
                    f"Starting analysis of project {project_id}", type="info"
                )
                run_analysis(output_dir, project_id, analyzers)
                console_output("Analysis complete.", type="info")
                socketio.emit("analysis_complete", {"status": "success"}, namespace="/")
            else:
                socketio.emit("decompile_complete", {"status": "error"}, namespace="/")

            # Clean up the uploaded file
            print(f"Removing uploaded file: {filepath}")
            console_output(f"Removing uploaded file: {filepath}", type="debug")
            os.remove(filepath)

        except Exception as e:
            error_msg = f"An error occurred: {str(e)}"
            logging.error(error_msg)
            console_output(error_msg, type="error")
            socketio.emit("decompile_complete", {"status": "error"}, namespace="/")

    socketio.start_background_task(run_decompilation_and_analysis)


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
    console_output("Starting wipe of decompiled files...", type="info")

    folders = []
    for item in os.listdir(DECOMPILE_FOLDER):
        item_path = os.path.join(DECOMPILE_FOLDER, item)
        if os.path.isdir(item_path):
            console_output(f"Removing folder: {item_path}", type="debug")
            folders.append(item)
            shutil.rmtree(item_path)
        elif os.path.isfile(item_path):
            console_output(f"Removing file: {item_path}", type="debug")
            os.remove(item_path)

    return jsonify({"message": "Decompiled files wiped", "folders": folders})


@app.route("/file/<path:filepath>", methods=["GET"])
def get_file(filepath):
    full_path = os.path.join(DECOMPILE_FOLDER, filepath)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return send_file(full_path)
    else:
        return jsonify({"error": "File not found", "path": full_path}), 404


@app.route("/endpoints/<int:project_id>", methods=["GET"])
def get_endpoints(project_id):
    endpoints = get_project_endpoints(project_id)
    return jsonify(endpoints)


@app.route("/firebase_keys/<int:project_id>", methods=["GET"])
def get_firebase_keys(project_id):
    firebase_keys = get_project_firebase_keys(project_id)
    return jsonify(firebase_keys)


def console_output(data, type="info"):
    socketio.emit(
        "console_output",
        {"data": data, "type": type},
        namespace="/",
    )


if __name__ == "__main__":
    print("🚀 Starting APK Decompiler Backend")
    print(
        f"Database path: {os.environ.get('SQLITE_DB_PATH', 'sqlite:///api_discovery.db')}"
    )

    socketio.run(
        app,
        host="0.0.0.0",
        port=os.getenv("PORT", 5000),
        debug=True,
        use_reloader=False,
        log_output=True,
    )
