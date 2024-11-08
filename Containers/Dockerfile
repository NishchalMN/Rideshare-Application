FROM python:3.7-slim-stretch

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN mkdir -p /code
RUN apt update
RUN apt install -y libpq-dev python-dev
RUN apt install -y default-libmysqlclient-dev
RUN apt install -y default-mysql-server
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
COPY . /code
WORKDIR /code