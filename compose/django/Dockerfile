FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

RUN apk add --no-cache tzdata \
    && ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime

RUN pip install --no-cache-dir -U -r /requirements/production.txt

COPY . /app
COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh

RUN addgroup django \
    && adduser -D -G django django \
    && chown -R django /app \
    && sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
