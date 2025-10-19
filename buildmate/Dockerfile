FROM python:3.12-slim

# Set working directory
WORKDIR /buildmate

# Install MinGW-w64 (for cross-compiling to Windows) and essential build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        mingw-w64 \
        build-essential \
        libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .
