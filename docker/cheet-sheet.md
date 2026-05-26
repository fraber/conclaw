# Conclaw (Nanobot) Docker Cheat Sheet

This document contains useful Docker commands for building, running, and debugging the `conclaw` image.

## 1. Build the Docker Image

To build the image from the `Dockerfile` in the current directory:

```bash
docker build -t conclaw-app .
```

To **re-build** the image from scratch without using cached layers (e.g. if you updated the GitHub repository but Docker keeps using the old cached clone):

```bash
docker build --no-cache -t conclaw-app .
```

## 2. Run the Docker Container

Run the image in the background (`-d`), mapping port 8080 to your host, creating a persistent volume `/path/on/host/data` mapped to `/data`, and connecting to your host's Ollama instance.

**For Linux hosts (requires `--add-host` to resolve `host.docker.internal`):**

```bash
docker run -d \
  --name conclaw-instance \
  -p 8080:8080 \
  -p 18790:18790 \
  -p 8900:8900 \
  -p 8765:8765 \
  -v /home/fraber/dev/aria/docker/data:/data \
  --add-host=host.docker.internal:host-gateway \
  conclaw-app
```

Secure alternative:

```bash
docker run -d \
  --name conclaw-instance \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  -p 127.0.0.1:8080:8080 \
  -p 127.0.0.1:18790:18790 \
  -p 127.0.0.1:8900:8900 \
  -p 127.0.0.1:8765:8765 \
  -v /home/fraber/dev/aria/docker/data:/data:rw \
  --add-host=host.docker.internal:host-gateway \
  conclaw-app
```

## 3. Stop and Delete the Container

Stop the running container:

```bash
docker stop conclaw-instance
```

Remove the stopped container:

```bash
docker rm conclaw-instance
```

## 4. Delete the Image

If you want to remove the built image from your system to free up space:

```bash
docker rmi conclaw-app
```

## 5. Debugging and Accessing the Container

### Connect to a running container as `root` with bash

If you need to enter a **running** container as the root user for debugging, package installation, etc:

```bash
docker exec -u root -it conclaw-instance /bin/bash
```

*(If you want to enter as the normal `conclaw` user instead, just omit `-u root`)*

### Connect to a stopped container / Debugging Startup Issues

If the container fails to start (e.g. because of an issue with the ENTRYPOINT), you cannot use `docker exec`. Instead, start a brand new temporary container overriding the entrypoint so you get directly into a Bash shell:

```bash
docker run --rm -it --add-host=host.docker.internal:host-gateway --entrypoint bash conclaw-app
```

To run as root in this scenario:
```bash
docker run --rm -u root -it --add-host=host.docker.internal:host-gateway --entrypoint bash conclaw-app
```

### View output (STDOUT / STDERR)

To see the live console output from the `conclaw gateway` process (which includes both backend logs and Web GUI logs):

```bash
docker logs -f conclaw-instance
```
*Press `Ctrl+C` to exit the log view.*

## 6. Important Notes

- **Ollama**: Ensure your local Ollama is running and accessible. `host.docker.internal:11434` assumes Ollama runs on port 11434 on the computer hosting Docker.
- **Persistent State**: Any database or configuration written to `/data` inside the container is saved to the folder you specify with `-v` on your host machine. This survives container restarts and deletions.
- **Port Mapping**: `-p 8080:8080` maps the container's port 8080 to your computer's port 8080. You can access the Web GUI at `http://localhost:8080`.
