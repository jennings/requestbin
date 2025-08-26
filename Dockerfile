FROM    python:3.13

# Add uv
COPY    --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /opt/requestbin

# install dependencies
COPY    pyproject.toml uv.lock ./
RUN     uv sync --locked

# the code
COPY    requestbin  ./requestbin

# runtime
ENV	REQUESTBIN_WORKERS=2
ENV	REQUESTBIN_MAX_REQUESTS=1000
EXPOSE  8000
CMD     uv run gunicorn -b 0.0.0.0:8000 \
	--worker-class gevent \
	--workers ${REQUESTBIN_WORKERS} \
	--max-requests ${REQUESTBIN_MAX_REQUESTS} \
	requestbin:app
