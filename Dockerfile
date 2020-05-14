FROM python:3.7

ENV FLASK_APP=/var/www/html/app.py
ENV FLASK_ENV=development

RUN apt-get update
RUN pip install poetry

WORKDIR /var/www/html/
COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install

CMD flask run --host 0.0.0.0