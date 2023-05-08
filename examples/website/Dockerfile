FROM python:3.8-slim-buster

RUN pip install django

ADD app/ /app
WORKDIR /app

ENTRYPOINT ["python", "manage.py"]
