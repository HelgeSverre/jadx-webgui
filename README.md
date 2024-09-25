# 🌩️ APK Decompiler - In the *Cloud* 😱

## ✨ Overview

This project demonstrates real-time output streaming from a backend process to a frontend using SocketIO and Python.
It uses [JADX](https://github.com/skylot/jadx) to decompile an uploaded APK file, streaming the output to the frontend
in real-time. Additional features
include browsing decompiled files and scanning for URLs and Firebase keys.

The project serves as a testbed for ideas, exploring how to build upon this concept. It's not intended for production
use but as a learning tool for working with websockets, Docker, and Flask, and building tools for APK analysis.

Feel free to fork and play around with it.

## 🚀 Features

- **Real-Time Output Streaming**: Uses SocketIO to stream live output from the backend process (JADX) to the frontend,
  providing immediate feedback.
- **Wrapping a Complex Process**: Demonstrates how to handle and stream output from a non-trivial task like APK
  decompilation.
- **Dockerized Environment**: Both backend and frontend are containerized using Docker, making it easy to build and run
  the application.
- **Tech Stack**:
    - **Backend**: Flask (Python) for the API, with SocketIO for real-time communication.
    - **Frontend**: Svelte with TailwindCSS for building a responsive user interface.

## 🛠️ Setup and Installation

### Clone the Repository

Clone the repository to your local machine:

```shell
git clone git@github.com:HelgeSverre/jadx-webgui.git
cd jadx-webgui
```

### Quick Start with Docker Compose

To build and run the application using Docker Compose:

```shell
# Build and run the containers
docker compose up --build -d

# Stop and remove containers
docker compose down
```

Access the application at `http://localhost:8080`.

### Backend Setup

To build and run the backend separately:

```shell
# Navigate to the API directory
cd api

# Format the Python code
pipx run black app.py

# Build the Docker image
docker build -t decompiler-backend .

# Run the Docker container
docker run -p 8080:5000 \
  -v $(pwd)/uploads:/tmp/uploads \
  -v $(pwd)/decompiled:/tmp/decompiled \
  decompiler-backend

# Or as a one-liner
docker build -t decompiler-backend . && docker run -p 8080:5000 -v $(pwd)/uploads:/tmp/uploads -v $(pwd)/decompiled:/tmp/decompiled decompiler-backend
```

### Frontend Setup

#### Using Docker 🐳

```shell
# Build the Docker image
docker build -t decompiler-frontend .

# Run the Docker container
docker run -p 3000:3000 decompiler-frontend
```

#### Without Docker 🚀

```shell
# Navigate to the web directory
cd web

# Install dependencies
yarn install

# Format the code
yarn format

# Run the development server
yarn dev
```

## 🧹 Code Formatting

To maintain code consistency:

```shell
# Format backend Python code
pipx run black api/app.py

# Format frontend code
yarn --cwd web format

# One-liner for both
pipx run black api/app.py && yarn --cwd web format
```

## 📝 Notes

This project is primarily an experiment to see how to stream output from a backend process to the frontend in real-time
using sockets. It serves as a practical example of handling complex tasks within a Dockerized environment and streaming
their output, rather than focusing solely on the APK decompilation.

## ⚠️ Disclaimer

> This project is provided for educational and research purposes only. The authors and contributors are not responsible
> for any misuse or damage that may result from using this tool. Users should ensure they have the right to decompile
> and
> analyze any APK files they process with this tool.
>
> Remember that decompiling applications without permission may violate terms of service, copyright laws, or other legal
> agreements. Always respect intellectual property rights and use this tool responsibly and ethically.
>
> By using this software, you agree to these terms and acknowledge that you use it at your own risk.

You know the drill.