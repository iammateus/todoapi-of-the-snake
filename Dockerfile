FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN apt-get update
RUN pip install poetry

WORKDIR /app
COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install