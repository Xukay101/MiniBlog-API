# Makefile

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

init-db:
	docker-compose run api flask db init

migrate:
	docker-compose run api flask db migrate

upgrade:
	docker-compose run api flask db upgrade

shell:
	docker-compose run api flask shell

test:
	docker-compose run api pytest

.PHONY: build up down init-db migrate upgrade shell test
