FROM python:3.12-slim
WORKDIR /buildmate
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install --no-cache-dir -e .
ENV PYTHONPATH=/buildmate
CMD ["python", "app/main.py"]