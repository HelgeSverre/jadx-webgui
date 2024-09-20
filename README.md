# Web based Decompiler using docker

### Just the backend

## Build

```shell
docker build -t decompiler .
```

## Run

```shell
docker run -p 5000:5000 -v $(pwd)/uploads:/tmp/uploads -v $(pwd)/decompiled:/tmp/decompiled decompiler
```

### Compose

```shell
docker-compose up --build
```

```shell
docker-compose down
```