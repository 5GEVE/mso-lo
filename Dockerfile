FROM python:3.6 as base
EXPOSE 5000
RUN apt-get update && apt-get install -y python3-dev
RUN ["pip3", "install", "pipenv"]
ENV PIPENV_VENV_IN_PROJECT 1
WORKDIR /usr/src/app
# copy only pipfiles to install dependencies
COPY ./adaptation_layer/Pipfile .
COPY ./adaptation_layer/Pipfile.lock .
RUN ["pipenv", "install"]
COPY ./adaptation_layer .

## setup env variables to initialize database
#ARG DB_SEED_NFVO
#ENV DB_SEED_NFVO $DB_SEED_NFVO
#ARG DB_SEED_NFVO_CRED
#ENV DB_SEED_NFVO_CRED $DB_SEED_NFVO_CRED
#RUN ["rm", "-f", "data/mso-lo.db"]
#RUN ["pipenv", "run", "flask", "db", "upgrade"]
#RUN ["pipenv", "run", "python", "manage.py", "seed"]

FROM base as prod
COPY ./uWSGI/app.ini .
CMD ["pipenv", "run", "uwsgi", "--ini", "app.ini"]