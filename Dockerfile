FROM python:3.6 as base
RUN apt-get update && apt-get install -y python3-dev
ENV PIPENV_VENV_IN_PROJECT 1
RUN ["pip3", "install", "pipenv"]
WORKDIR /usr/src/app
EXPOSE 5000

FROM base as dev
# copy only pipfiles to install dependencies
COPY ./adaptation_layer/Pipfile .
COPY ./adaptation_layer/Pipfile.lock .
RUN ["pipenv", "install", "--dev"]
# Bind mount here?

FROM base as test
COPY ./adaptation_layer .
RUN ["pipenv", "install", "--dev"]
ENV TESTING True

FROM base as prod
COPY ./adaptation_layer .
COPY ./uWSGI/app.ini .
RUN ["pipenv", "install"]
CMD pipenv run uwsgi --ini app.ini

