#!/bin/bash

# Build the Docker image
docker build -t backend .

# Run the Docker container
docker run -it\
  -p 8080:5000 \
  -v $(pwd)/uploads:/tmp/uploads \
  -v $(pwd)/decompiled:/tmp/decompiled \
  -v $(pwd)/data:/data \
  -e SQLITE_DB_PATH=sqlite:////data/api_discovery.db \
  backend

echo "🚀 APK Analyzer backend is starting"