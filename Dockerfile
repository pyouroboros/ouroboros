FROM python:3.6-alpine

COPY . /app
WORKDIR /app
RUN pip install .
ENTRYPOINT ["ouroboros"]