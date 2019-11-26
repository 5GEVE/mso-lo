FROM python:3.6 as base
RUN apt-get update && apt-get install -y python-dev python3-dev
RUN ["pip3", "install", "pipenv"]
WORKDIR /usr/src/app
COPY ./adaptation_layer .
EXPOSE 5000

FROM base as dev
RUN ["pipenv", "install", "--dev"]
CMD pipenv run python app.py

#FROM base as test

#FROM base as prod

