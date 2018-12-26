FROM python:3.6-alpine

COPY . /app
WORKDIR /app
RUN apk add --no-cache tzdata && \
    pip install --no-cache-dir .
ENTRYPOINT ["ouroboros"]