FROM python:3.6 as base
RUN apt-get update && apt-get install -y python3-dev
ENV PIPENV_VENV_IN_PROJECT 1
RUN ["pip3", "install", "pipenv"]
WORKDIR /usr/src/app
COPY ./adaptation_layer .
EXPOSE 5000

FROM base as dev
RUN ["pipenv", "install", "--dev"]
CMD pipenv run python app.py

#FROM base as test

FROM base as prod
RUN ["pipenv", "install"]
COPY ./uWSGI/app.ini .
CMD pipenv run uwsgi --ini app.ini

