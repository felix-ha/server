.PHONY: docker_build_python_server
docker_build_python_server:
	docker build -t python-server . 

.PHONY: up
up:
	docker compose up -d
