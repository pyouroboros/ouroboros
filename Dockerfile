FROM amd64/python:3.12.0a4-alpine3.17

LABEL maintainers="dirtycajunrice,circa10a"

ENV TZ UTC

WORKDIR /app

COPY /requirements.txt /setup.py /ouroboros /README.md /app/

RUN apk add --no-cache tzdata && \
    pip install --no-cache-dir -r requirements.txt

COPY /pyouroboros /app/pyouroboros

RUN pip install --no-cache-dir .

ENTRYPOINT ["ouroboros"]
