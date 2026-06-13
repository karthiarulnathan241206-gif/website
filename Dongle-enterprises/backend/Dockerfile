FROM python:3.11-slim

WORKDIR /app

# Install build deps and cleanup to keep image small
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

# Copy app source
COPY . /app

# Do not copy credentials.json into image; mount at runtime or use secrets
ENV PORT=5000

EXPOSE ${PORT}

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
