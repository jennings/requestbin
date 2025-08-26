DOCKER_CLI := docker

.PHONY: all
all: run

.PHONY: run
run:
	uv run gunicorn requestbin:app

.PHONY: build
build:
	$(DOCKER_CLI) build -t requestbin .
