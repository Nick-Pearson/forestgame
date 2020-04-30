FROM python:3-alpine

COPY ./server/requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

COPY server /app
COPY dist /dist

CMD [ "python", "/app/main.py" ]