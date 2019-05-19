FROM amd64/python:3.7.2-alpine

LABEL maintainers="dirtycajunrice,circa10a"

ENV TZ UTC

WORKDIR /app

COPY /requirements.txt /setup.py /ouroboros /README.md /app/

RUN apk add --no-cache dumb-init tzdata && \
    pip install --no-cache-dir -r requirements.txt

COPY /pyouroboros /app/pyouroboros

RUN pip install --no-cache-dir .

ENTRYPOINT ["dumb-init"]
CMD ["/app/ouroboros"]
