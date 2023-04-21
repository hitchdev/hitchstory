FROM python:3.8-slim-buster

RUN pip install flask textblob

ADD app/ /app

ENTRYPOINT ["python", "/app/main.py"]
