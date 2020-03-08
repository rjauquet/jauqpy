CODE := {{ cookiecutter.import_name }}
# if we move pyproject.toml, fist cd its directory
POETRY := poetry

INSTALL_FLAG := .flag-install

.PHONY: setup
setup:
	-cp -n .env-example .env
	./bin/verchew

.PHONY: install
install:
	md5sum -c $(INSTALL_FLAG) --status || \
		$(POETRY) install && md5sum poetry.lock pyproject.toml >| $(INSTALL_FLAG)

.PHONY: run_db
run_db:
	docker-compose up -d db

.PHONY: run_redis
run_redis:
	docker-compose up -d redis

.PHONY: run_web
run_web: install run_redis migrate
	$(POETRY) run python manage.py runserver 0.0.0.0:8{{ cookiecutter.id }}

.PHONY: run_task
run_task: install run_redis migrate
	$(POETRY) run python manage.py run_huey

.PHONY: run
run: install migrate
	docker-compose up

.PHONY: migrate
migrate: install run_db
	$(POETRY) run python manage.py migrate

.PHONY: check
check: install
	$(POETRY) run isort $(CODE) --recursive --apply
	$(POETRY) run black $(CODE)
	$(POETRY) run mypy $(CODE) --config-file=.mypy.ini
	$(POETRY) run pylint $(CODE)

.PHONY: test
test: install migrate
	$(POETRY) run pytest $(CODE) --quiet

