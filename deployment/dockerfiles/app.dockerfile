FROM python:3.11-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get -y install netcat-traditional gcc && \
    apt-get -y install cron && \
    apt-get -y install libpq-dev gcc && \
    apt-get clean && \
    alias py=python

COPY src/requirements.txt ./requirements.txt

RUN pip install pip --upgrade \
    && pip install -r requirements.txt

COPY deployment/scripts /app/deployment/scripts

# django-crontab logfile
RUN mkdir /cron
RUN touch /cron/django_cron.log

RUN chmod -R +x /app/deployment/scripts/*

COPY src/ ./
