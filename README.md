# 🌩️ APK Decompiler - In the Cloud

An experimental project demonstrating real-time event streaming from a Docker container to a frontend, showcasing
non-trivial operations like cloud-based APK decompilation.

## 🚀 Features

- Uses JADX for APK decompilation
- Python Flask backend
- SocketIO for real-time backend-frontend communication
- Svelte and TailwindCSS frontend

## 🛠️ Setup and Installation

### Quick Start with Docker Compose

```shell
# Build and run
docker compose up --build -d

# Tear down
docker compose down
```

Now open your browser and go to `http://localhost:8080` to see the app in action.

### Backend

```shell
# Change directory
cd api

# Format the code
pipx run black app.py

# Build
docker build -t decompiler-backend .

# Run 
docker run -p 8080:5000 -v $(pwd)/uploads:/tmp/uploads -v $(pwd)/decompiled:/tmp/decompiled decompiler-backend

# One-liner
docker build -t decompiler-backend . && docker run -p 8080:5000 -v $(pwd)/uploads:/tmp/uploads -v $(pwd)/decompiled:/tmp/decompiled decompiler-backend
```

### Frontend (Docker)  🐳

```shell
docker build -t decompiler-frontend .
docker run -p 3000:3000 decompiler-frontend
```

### Frontend (Without Docker) 🚀

```shell
# Change directory
cd web

# Install dependencies
yarn install

# Format the code
yarn format

# Run
yarn dev
```

----

## 🧹 Code Formatting

To format both backend and frontend code:

```shell
# Format backend
pipx run black api/app.py

# Format frontend
yarn --cwd web format

# One-liner for both
pipx run black api/app.py && yarn --cwd web format
```