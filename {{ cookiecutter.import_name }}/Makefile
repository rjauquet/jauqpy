.DEFAULT_GOAL := help

SHELL := /bin/bash
CODE := {{ cookiecutter.import_name }}
# if we move pyproject.toml, fist cd its directory
POETRY := poetry

ECR_REGISTRY ?=
BASE_IMAGE_TAG ?= latest

INSTALL_FLAG := .flag-install

-include .env

## -- Setup and Install --

## handles any pre-req setup including creating an .env
.PHONY: setup
setup:
	-@cp -n .env-example .env || true
	./bin/verchew

## installs python dependencies, skipping if there are no known changes
.PHONY: install
install: setup
	@md5sum -c $(INSTALL_FLAG) --status || \
		$(POETRY) update && md5sum poetry.lock pyproject.toml >| $(INSTALL_FLAG)


## -- Databases --

## build and start postgres
.PHONY: database
database:
	docker-compose up -d db

## build and start redis
.PHONY: redis
redis:
	docker-compose up -d redis

## -- Services --

## starts the django development server
.PHONY: django
django: install redis migrate
	$(POETRY) run python manage.py runserver 0.0.0.0:8{{ cookiecutter.id }}

## starts the Celery server
.PHONY: celery
celery: install database redis migrate
	$(POETRY) run celery -A {{ cookiecutter.import_name }}.tasks.tasks worker --loglevel=info

## starts the Celery Beat scheduler
.PHONY: beat
beat: install database redis migrate
	$(POETRY) run celery -A {{ cookiecutter.import_name }}.tasks.tasks beat --loglevel=info

## -- Actions --

## creates a superuser
.PHONY: superuser
superuser: install
	$(POETRY) run python manage.py createsuperuser

## generates new migration files
.PHONY: migrations
migrations: install database
	$(POETRY) run python manage.py makemigrations

## updates the database with latest migrations
.PHONY: migrate
migrate: install database
	$(POETRY) run python manage.py migrate

## formats and checks code
.PHONY: check
check: install
ifeq ($(CICD),1)
	$(POETRY) run isort --diff $(CODE)
	$(POETRY) run black --check $(CODE)
	$(POETRY) run mypy $(CODE) --config-file=.mypy.ini
	$(POETRY) run pylint $(CODE)
	$(POETRY) run python manage.py makemigrations --check --dry-run
	# terraform fmt will be checked by its own workflow in CICD
else
	$(POETRY) run isort $(CODE)
	$(POETRY) run black $(CODE)
	$(POETRY) run mypy $(CODE) --config-file=.mypy.ini
	$(POETRY) run pylint $(CODE)
	$(POETRY) run python manage.py makemigrations --check --dry-run
	terraform -chdir=terraform fmt -recursive
endif

## runs all tests
.PHONY: test
test: install migrate
	$(POETRY) run pytest --cov-config=.coveragerc \
		--cov=$(CODE) $(CODE) --cov-fail-under=90 --quiet

## starts a django shell ipython session
.PHONY: shell
shell: install database
	$(POETRY) run python manage.py shell_plus

## logs into aws
.PHONY: aws-login
aws-login:
	aws ecr get-login-password --region us-east-1 | \
		docker login --username AWS --password-stdin ${ECR_REGISTRY}

## outputs this help message
.PHONY: help
help:
	@printf "Usage\n";

	@awk '{ \
			if ($$0 ~ /^.PHONY: [a-zA-Z\-\_0-9]+$$/) { \
				helpCommand = substr($$0, index($$0, ":") + 2); \
				if (helpMessage) { \
					printf "\033[36m%-20s\033[0m %s\n", \
						helpCommand, helpMessage; \
					helpMessage = ""; \
				} \
			} else if ($$0 ~ /^[a-zA-Z\-\_0-9.]+:/) { \
				helpCommand = substr($$0, 0, index($$0, ":")); \
				if (helpMessage) { \
					printf "\033[36m%-20s\033[0m %s\n", \
						helpCommand, helpMessage; \
					helpMessage = ""; \
				} \
			} else if ($$0 ~ /^##/) { \
				if (helpMessage) { \
					helpMessage = helpMessage"\n                     "substr($$0, 3); \
				} else { \
					helpMessage = substr($$0, 3); \
				} \
			} else { \
				if (helpMessage) { \
					print "                     "helpMessage"" \
				} \
				helpMessage = ""; \
			} \
		}' \
		$(MAKEFILE_LIST)
