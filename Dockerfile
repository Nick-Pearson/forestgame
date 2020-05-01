FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
ENV LISTEN_PORT 8080

COPY ./custom-start.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./server/requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY server /app
COPY uwsgi.ini /app/uwsgi.ini
COPY dist /dist