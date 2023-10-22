FROM python:3.8-slim-buster


ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install netcat -y


RUN pip install flask textblob

ADD app/ /app

ENTRYPOINT ["python", "/app/api.py"]
