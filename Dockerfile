FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.8

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

COPY ./custom-start.sh /custom-start.sh
RUN chmod +x /custom-start.sh

COPY ./server/requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY server /app
COPY dist /dist

CMD ["/custom-start.sh"]