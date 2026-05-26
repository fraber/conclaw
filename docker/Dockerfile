# Use the official Python image which allows global pip installations
FROM python:3.12-slim

# Create a system group and user named 'conclaw' with a home directory
RUN groupadd -g 1000 conclaw && \
    useradd -u 1000 -g conclaw -m -s /bin/bash conclaw

ENV PATH="/home/conclaw/.local/bin:${PATH}"

# Allow global pip installation in Python 3.12+
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# Install system dependencies required for background tools, git, and Node.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    coreutils systemctl wget iputils-ping net-tools netcat-openbsd \
    telnet git emacs-nox curl ca-certificates gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_21.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Upgrade pip and install conclaw from github fork
RUN pip install --no-cache-dir --upgrade pip
RUN git clone https://github.com/fraber/conclaw.git /app \
    && pip install -e /app

# Install dependencies and build the nanobot WebUI
WORKDIR /app/webui
RUN npm install && npm run build

# Copy start script
COPY start.sh /app/start.sh

# Ensure proper permissions for the user
RUN chmod +x /app/start.sh && \
    chown -R conclaw:conclaw /app && \
    mkdir -p /data && chown -R conclaw:conclaw /data

# Configure persistent data volume path and Ollama Host connection
ENV CONCLAW_STATE=/data/conclaw.db
ENV OLLAMA_HOST=http://host.docker.internal:11434
VOLUME ["/data"]

# Expose the ports for WebUI (8080), Gateway (18790), API (8900), and Websockets (8765)
EXPOSE 8080 18790 8900 8765

USER conclaw
RUN echo 'alias "l=ls -als"' >> ~/.bashrc
WORKDIR /app

# Run the initialization and start the gateway
ENTRYPOINT ["/app/start.sh"]
CMD ["gateway"]
