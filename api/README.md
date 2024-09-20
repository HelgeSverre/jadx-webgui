# Decompiler Backend API

Provides an API to decompile APK files via jadx, also streams events to the client via SocketIO.

```shell
# Build
docker build -t backend .

# Run 
docker run -p 8080:5000 -v $(pwd)/uploads:/tmp/uploads -v $(pwd)/decompiled:/tmp/decompiled backend
```

### One-liner

```shell
docker build -t backend . && docker run -p 8080:5000 -v $(pwd)/uploads:/tmp/uploads -v $(pwd)/decompiled:/tmp/decompiled backend
```

## Format the code

```shell
pipx run black app.py
```