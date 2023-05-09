FROM python:3.8-slim-buster

ADD app/ /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "manage.py"]
