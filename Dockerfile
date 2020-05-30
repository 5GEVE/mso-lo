FROM python:3.6-slim as base
EXPOSE 5000
RUN apt-get update && apt-get install -y build-essential
RUN ["pip3", "install", "pipenv==2018.11.26"]
ENV PIPENV_VENV_IN_PROJECT 1
WORKDIR /usr/src/app
# copy only pipfiles to install dependencies
COPY ./adaptation_layer/Pipfile* ./
RUN ["pipenv", "install", "--system", "--ignore-pipfile", "--deploy"]
COPY ./adaptation_layer .
# setup env variables to initialize database
ARG DB_SEED_NFVO
ENV DB_SEED_NFVO $DB_SEED_NFVO
ARG DB_SEED_NFVO_CRED
ENV DB_SEED_NFVO_CRED $DB_SEED_NFVO_CRED
RUN ["rm", "-f", "data/mso-lo.db"]
RUN ["flask", "db", "upgrade"]
RUN ["python", "manage.py", "seed"]

FROM base as prod
COPY ./uWSGI/app.ini .
CMD ["uwsgi", "--ini", "app.ini"]

FROM base as test
COPY ./openapi ./openapi

