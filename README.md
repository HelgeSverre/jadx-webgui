# Web based Decompiler using docker

## Build

```shell
docker build -t decompiler .
```

## Run

```shell
docker run -p 5000:5000 -v $(pwd)/uploads:/tmp/uploads -v $(pwd)/decompiled:/tmp/decompiled decompiler
```


