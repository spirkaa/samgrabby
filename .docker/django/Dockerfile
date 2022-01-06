FROM registry.home.devmem.ru/python:3.9-alpine

ENV PYTHONUNBUFFERED=1
ARG CRYPTOGRAPHY_DONT_BUILD_RUST=1

COPY .docker/django/rootfs /

COPY samgrabby/requirements /app/requirements

RUN set -eux \
    && pip install --no-cache-dir -U -r /app/requirements/production.txt

COPY samgrabby /app

WORKDIR /app