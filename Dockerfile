FROM python:3.11-slim-buster

WORKDIR /flaskr_blog

ENV APP_SETTINGS='flaskr.config.ProductionConfig'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install waitress
COPY . .

CMD waitress-serve --host 0.0.0.0 --call flaskr:create_app