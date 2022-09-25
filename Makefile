.DEFAULT_GOAL := service

POETRY := poetry

.PHONY: install
install:
	$(POETRY) update

.PHONY: service
service: install
	$(POETRY) run cookiecutter . -o ../

