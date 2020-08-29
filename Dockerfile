FROM python:3.6-slim as base
EXPOSE 5000
RUN apt-get update && apt-get install -y build-essential
RUN ["pip3", "install", "pipenv==2020.6.2"]
WORKDIR /usr/src/app/
# copy only pipfiles to install dependencies
COPY ./adaptation_layer/Pipfile* ./
RUN ["pipenv", "install", "--system", "--ignore-pipfile", "--deploy"]
COPY ./adaptation_layer ./adaptation_layer
# setup env variables to initialize database
ARG DB_SEED_NFVO
ENV DB_SEED_NFVO $DB_SEED_NFVO
ARG DB_SEED_NFVO_CRED
ENV DB_SEED_NFVO_CRED $DB_SEED_NFVO_CRED
ENV FLASK_APP adaptation_layer
RUN ["rm", "-f", "adaptation_layer/data/mso-lo.db"]
RUN ls -la
RUN ["flask", "db", "upgrade"]
RUN ["flask", "seed"]

FROM base as prod
COPY ./uWSGI .
CMD ["uwsgi", "--ini", "app.ini"]

FROM base as test
RUN ["pipenv", "install", "--system", "--ignore-pipfile", "--deploy", "--dev"]
COPY ./openapi ./openapi

