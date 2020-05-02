FROM tiangolo/uwsgi-nginx-flask:python3.7

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

# Heroku hack fix - listen from $PORT rather than $LISTEN_PORT
RUN sed -i 's/LISTEN_PORT/PORT/g' /entrypoint.sh
RUN cat /entrypoint.sh

COPY ./server/requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# COPY server /app/app
# COPY uwsgi.ini /app/uwsgi.ini
COPY dist /dist