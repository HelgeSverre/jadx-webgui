import os
import subprocess
import logging
from flask import Flask, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit

logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")


UPLOAD_FOLDER = '/tmp/uploads'
DECOMPILE_FOLDER = '/tmp/decompiled'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DECOMPILE_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        socketio.start_background_task(decompile_apk, filepath)
        return jsonify({"message": "File uploaded and decompilation started"}), 200


def decompile_apk(filepath):
    output_dir = os.path.join(DECOMPILE_FOLDER, os.path.splitext(os.path.basename(filepath))[0])
    try:
        process = subprocess.Popen(['jadx', '-d', output_dir, filepath],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   universal_newlines=True)

        for line in process.stdout:
            print(line, end='')  # Print to server console
            socketio.emit('console_output', {'data': line.strip()})

        process.wait()
        if process.returncode == 0:
            socketio.emit('decompile_complete', {'status': 'success'})
        else:
            socketio.emit('decompile_complete', {'status': 'error'})
    except FileNotFoundError:
        error_msg = "JADX not found. Please ensure it's installed and in the system PATH."
        logging.error(error_msg)
        socketio.emit('console_output', {'data': error_msg})
        socketio.emit('decompile_complete', {'status': 'error'})
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        logging.error(error_msg)
        socketio.emit('console_output', {'data': error_msg})
        socketio.emit('decompile_complete', {'status': 'error'})


@app.route('/files', methods=['GET'])
def list_files():
    files = []
    for root, dirs, filenames in os.walk(DECOMPILE_FOLDER):
        for filename in filenames:
            relative_path = os.path.relpath(os.path.join(root, filename), DECOMPILE_FOLDER)
            files.append(relative_path)
    return jsonify({"files": files})


@app.route('/file/<path:filepath>', methods=['GET'])
def get_file(filepath):
    full_path = os.path.join(DECOMPILE_FOLDER, filepath)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return send_file(full_path)
    else:
        return jsonify({
            "error": "File not found",
            "path": full_path
        }), 404


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
