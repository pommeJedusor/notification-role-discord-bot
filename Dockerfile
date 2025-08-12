FROM python:3.13-alpine

RUN apk add --no-cache \
    libffi-dev \
    libsodium-dev \
    python3-dev \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
