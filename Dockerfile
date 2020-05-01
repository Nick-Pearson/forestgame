FROM tiangolo/uwsgi-nginx-flask:python3.7-alpine3.8

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
ENV LISTEN_PORT 8080

COPY ./server/requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY server /app
COPY dist /dist