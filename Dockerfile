FROM python:3.7-alpine

COPY / /app

WORKDIR /app

RUN apk add --no-cache tzdata && \
    pip install --no-cache-dir .

ENTRYPOINT ["python3", "ouroboros"]
