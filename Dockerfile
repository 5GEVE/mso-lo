FROM ubuntu:16.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && apt-get -y install git make python python3 \
    libcurl4-gnutls-dev libgnutls-dev tox python-dev python3-dev \
    python-setuptools python-all apt-utils python3-pip

RUN pip3 install pipenv uWSGI

COPY ./adaptation_layer /app
COPY ./uWSGI/app.ini /app/app.ini

WORKDIR /app

RUN pipenv install --system

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD [ "uwsgi", "--ini", "app.ini" ]
#CMD ["flask", "run", "--host", "0.0.0.0"]