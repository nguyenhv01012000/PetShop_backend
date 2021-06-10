#!/bin/bash
set -euxo pipefail
python manage.py migrate
echo "Starting web api"
python manage.py runserver 0.0.0.0:8000
#exec gunicorn -k uvicorn.workers.UvicornWorker config.asgi:application --bind unix:/tmp/gunicorn.sock