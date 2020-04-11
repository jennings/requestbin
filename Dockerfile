FROM    python:3-alpine

RUN     apk add --no-cache \
        gcc \
        make \
        python3-dev \
        libffi-dev \
        file \
        # greenlet
        musl-dev \
        # sys/queue.h
        bsd-compat-headers \
        # event.h
        libevent-dev

WORKDIR /opt/requestbin

# want all dependencies first so that if it's just a code change, don't have to
# rebuild as much of the container
ADD     requirements.txt .
RUN     pip install --no-cache-dir -r requirements.txt

# the code
ADD     requestbin  /opt/requestbin/requestbin/

EXPOSE  8000

CMD     gunicorn -b 0.0.0.0:8000 --worker-class gevent --workers 2 --max-requests 1000 requestbin:app


