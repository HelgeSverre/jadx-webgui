FROM openjdk:11-jdk-slim

# Install necessary dependencies
RUN apt-get update && apt-get install -y wget unzip python3 python3-pip

# Install JADX
RUN wget https://github.com/skylot/jadx/releases/download/v1.4.5/jadx-1.4.5.zip -O /tmp/jadx.zip && \
    unzip /tmp/jadx.zip -d /opt/jadx && \
    ln -s /opt/jadx/bin/jadx /usr/local/bin/jadx && \
    rm /tmp/jadx.zip

# Set up working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create necessary directories
RUN mkdir -p /tmp/uploads /tmp/decompiled

# Expose the application's port
EXPOSE 8080

# Command to run the application
CMD ["python3", "app.py", "--host", "0.0.0.0"]