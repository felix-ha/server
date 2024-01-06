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

## streamlit configuration

for streamlit to work behind a proxy, the following configuration in nginx proxy managers advanced settings is needed:
```bash
 location / {
        proxy_pass http://ip:port/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
```