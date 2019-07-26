FROM ubuntu:16.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV APP /app/adaptation_layer
RUN mkdir -p ${APP}
COPY . /app
RUN apt-get update && apt-get -y install git make python python3 \
    libcurl4-gnutls-dev libgnutls-dev tox python-dev python3-dev \
    debhelper python-setuptools python-all apt-utils python3-pip

RUN pip3 install pipenv uwsgi

WORKDIR /app/adaptation_layer


RUN pipenv install --system


EXPOSE 5000

#CMD [ "flask", "run",  ]