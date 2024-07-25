FROM python:3.11-slim

# Устанавливаем необходимые пакеты для работы psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev gcc


WORKDIR /app

COPY /requirements.txt /

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt --no-cache-dir

COPY . /app/
