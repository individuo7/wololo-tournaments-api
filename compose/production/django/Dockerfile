
FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add build-base
# psycopg2 dependencies
RUN apk add --virtual build-deps gcc python3-dev musl-dev
RUN apk add postgresql-dev
# Pillow dependencies
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
# CFFI dependencies
RUN apk add libffi-dev py-cffi

RUN addgroup -S django
RUN adduser -S -G django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements/production.txt
RUN rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
RUN chown django /start
COPY . /app

RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
