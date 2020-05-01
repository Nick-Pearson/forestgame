FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

COPY ./custom-entrypoint.sh /custom-entrypoint.sh

COPY ./server/requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY server /app
COPY dist /dist

ENTRYPOINT ["/custom-entrypoint.sh"]