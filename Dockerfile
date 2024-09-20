FROM openjdk:11-jdk-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y wget unzip python3 python3-pip

# Install JADX
RUN wget https://github.com/skylot/jadx/releases/download/v1.4.5/jadx-1.4.5.zip && \
    unzip jadx-1.4.5.zip -d /opt/jadx && \
    ln -s /opt/jadx/bin/jadx /usr/local/bin/jadx && \
    chmod +x /usr/local/bin/jadx && \
    rm jadx-1.4.5.zip

# Verify JADX installation
RUN jadx --version

# Set up Python environment
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY app.py .
COPY static/index.html static/

# Create necessary directories
RUN mkdir -p /tmp/uploads /tmp/decompiled

EXPOSE 5000

CMD ["python3", "app.py"]