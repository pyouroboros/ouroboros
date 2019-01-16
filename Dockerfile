FROM python:3.7-alpine

WORKDIR /app
COPY . .
RUN apk add --no-cache tzdata && \
    pip install --no-cache-dir .
ENTRYPOINT ["ouroboros"]
