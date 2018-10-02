FROM python:3-alpine
COPY . /
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "ouroboros/main.py"]