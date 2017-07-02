.PHONY: build run

all:
	@echo "not implemented"

build:
	docker build -t statusboard-ui .

run: build
	docker run -p 8002:80 -it statusboard-ui

dev: build run
