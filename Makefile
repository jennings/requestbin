.PHONY: all
all: run

.PHONY: run
run:
	gunicorn requestbin:app

.PHONY: docker
docker:
	docker build -t requestbin .
