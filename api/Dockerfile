FROM python:3.10-bullseye

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ARG GIT_VERSION
ARG GIT_BRANCH
ARG GIT_LASTCOMMITDATE

ENV GIT_VERSION=${GIT_VERSION}
ENV GIT_BRANCH=${GIT_BRANCH}
ENV GIT_LASTCOMMITDATE=${GIT_LASTCOMMITDATE}

VOLUME [ "/notebooks" ]

COPY ./requirements.txt /
COPY ./requirements.jupyter.txt /
RUN pip --disable-pip-version-check install --upgrade pip
RUN pip install -r /requirements.txt

RUN mkdir -p /app
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN mkdir -p /vol/backups

WORKDIR /app