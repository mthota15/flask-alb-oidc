FROM python:3.7-alpine3.8

WORKDIR /usr/src/app
EXPOSE 8080

COPY requirements.txt ./

RUN apk update \
    && apk add --no-cache --virtual .build-deps make gcc libc-dev  libffi-dev openssl-dev\
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY . .

STOPSIGNAL SIGTERM

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8080", "app:app"]
