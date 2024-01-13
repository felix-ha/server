.PHONY: up
up:
	docker compose up --remove-orphans -d
	
.PHONY: monitor
monitor:
	docker run --rm -e TZ="${TZ}" -v /var/run/docker.sock:/var/run/docker.sock:ro -v /run/user/1000/podman/podman.sock:/run/user/1000/podman/podman.sock:ro --pid host --network host -it nicolargo/glances:latest-full
