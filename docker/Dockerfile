FROM python:3.10.12-slim

WORKDIR app/

RUN python3 -m pip install --upgrade pip

COPY ./alembic/ /app/alembic
COPY ./app/ /app/app
COPY ./requirements.txt /app
COPY ./alembic.ini /app
COPY ./docker/server-entrypoint.sh /app

RUN pip install -r requirements.txt

RUN chmod +x ./server-entrypoint.sh
# CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
