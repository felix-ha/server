# server

## start
```bash
make up
```

## components

### ollama with web ui
needs to be build first
```bash
 docker compose -f docker-compose.yaml -f docker-compose.api.yaml up -d --build
```

stop ollama
```bash
 systemctl stop ollama
 ```