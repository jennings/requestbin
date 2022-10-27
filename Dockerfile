FROM    python:3.10-alpine

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

# configure Poetry
ENV POETRY_VERSION=1.2.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# install dependencies
COPY    pyproject.toml poetry.lock ./
RUN     poetry install

# the code
COPY    requestbin  ./requestbin

EXPOSE  8000
CMD     poetry run gunicorn -b 0.0.0.0:8000 --worker-class gevent --workers 2 --max-requests 1000 requestbin:app
