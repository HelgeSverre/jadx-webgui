# 🌩️ APK Decompiler - In the cloud

This is an experiment on how to stream events from a process running inside a docker container to a frontend to do
non-trivial and interesting things, like decompiling APKs in the cloud.

- Uses JADX to decompile APKs
- Python Flask for the backend
- SocketIO for the communication between the backend and the frontend
- Svelte and TailwindCSS for the frontend

--- 

## Setting up the project

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
cd frontend

# Install dependencies
yarn install

# Format the code
yarn format

# Run
yarn dev
```
