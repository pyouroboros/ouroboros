FROM python:3.7-alpine

WORKDIR /app

COPY / /app

RUN apk add --no-cache tzdata && \
    pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["ouroboros.py"]