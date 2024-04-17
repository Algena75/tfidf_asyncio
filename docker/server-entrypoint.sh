#!/bin/sh

# until cd /app/
# do
#     echo "Waiting for server volume..."
# done


until  alembic upgrade head 
do
    echo "Waiting for db to be ready..."
    sleep 2
done


# python manage.py collectstatic --noinput

# python manage.py createsuperuser --noinput

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
