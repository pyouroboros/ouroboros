FROM amd64/python:3.7.2-alpine

LABEL maintainers="dirtycajunrice,circa10a,tkdeviant"

ENV TZ UTC

WORKDIR /app

COPY /requirements.txt /setup.py /ouroboros /README.md /app/

COPY /pyouroboros /app/pyouroboros

RUN apk add --no-cache tzdata && \
    pip install --no-cache-dir .

ENTRYPOINT ["ouroboros"]