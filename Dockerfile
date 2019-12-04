FROM python:3.6 as base
RUN apt-get update && apt-get install -y python3-dev
ENV PIPENV_VENV_IN_PROJECT 1
ARG DB_SEED_NFVO
ENV DB_SEED_NFVO $DB_SEED_NFVO
ARG DB_SEED_NFVO_CRED
ENV DB_SEED_NFVO_CRED $DB_SEED_NFVO_CRED
RUN ["pip3", "install", "pipenv"]
WORKDIR /usr/src/app
EXPOSE 5000

FROM base as test
# copy only pipfiles to install dependencies
COPY ./adaptation_layer/Pipfile .
COPY ./adaptation_layer/Pipfile.lock .
RUN ["pipenv", "install", "--dev"]
# copy source code. if source changes we do not reinstall dependencies.
COPY ./adaptation_layer .

FROM base as prod
COPY ./adaptation_layer .
COPY ./uWSGI/app.ini .
RUN ["rm", "-f", "data/mso-lo.db"]
RUN ["pipenv", "install"]
RUN ["pipenv", "run", "flask", "db", "upgrade"]
RUN ["pipenv", "run", "python", "manage.py", "seed"]
CMD pipenv run uwsgi --ini app.ini

