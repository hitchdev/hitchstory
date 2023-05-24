FROM docker.io/python:3.8-slim-buster

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install netcat -y

ADD app/ /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["coverage", "run", "manage.py"]
