FROM python:3.8.0
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gettext \
    curl vim iputils-ping dnsutils && \
    rm -rf /var/lib/apt/lists/

RUN pip install --upgrade pip

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY manage.py /code
COPY entrypoint.sh /code
COPY config /code/config
COPY core /code/core
COPY apps /code/apps

RUN python manage.py compilemessages --locale vi --use-fuzzy
RUN mkdir -p /tmp/eureka/static && \
    python manage.py collectstatic --clear --noinput

CMD [ "/code/entrypoint.sh" ]

