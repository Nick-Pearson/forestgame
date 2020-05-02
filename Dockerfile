FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

RUN apk add --no-cache bash
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

# Heroku hack fix - listen from $PORT rather than $LISTEN_PORT
RUN sed -i 's/LISTEN_PORT:/PORT:/g' /entrypoint.sh

COPY ./server/requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# COPY server /app/app
# COPY uwsgi.ini /app/uwsgi.ini
COPY dist /dist

USER nginx