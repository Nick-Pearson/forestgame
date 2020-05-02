FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

RUN mv /entrypoint.sh /main-entrypoint.sh
COPY ./custom-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./server/requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY server /app/app
COPY uwsgi.ini /app/uwsgi.ini
COPY dist /dist