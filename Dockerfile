FROM python:3.6-alpine as base

FROM base as builder
RUN mkdir /deps
WORKDIR /deps
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/deps" -r /requirements.txt

FROM base
COPY --from=builder /deps /usr/local
COPY . /
WORKDIR /
ENTRYPOINT ["python3", "ouroboros/main.py"]