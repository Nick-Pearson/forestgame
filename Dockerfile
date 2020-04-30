FROM python:3-alpine

COPY ./server/requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

COPY ./server/*/*.py /app/
COPY ./server/main.py /app/main.py
COPY dist /dist

CMD [ "python", "/app/main.py" ]