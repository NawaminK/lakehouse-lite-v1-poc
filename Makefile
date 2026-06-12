SHELL := /bin/bash
DOCKER_SOCK ?= /var/run/docker.sock

.PHONY: help up down ps logs build reset smoke scenarios validate trino spark-create spark-quality superset-shell airflow-logs

help:
	@echo "Lakehouse Lite v1 POC commands"
	@echo "  make up             Start all core services"
	@echo "  make down           Stop services"
	@echo "  make ps             Show compose services"
	@echo "  make logs           Tail all logs"
	@echo "  make build          Build local images"
	@echo "  make reset          Reset POC data"
	@echo "  make smoke          Run smoke tests"
	@echo "  make scenarios      Run all POC scenarios"
	@echo "  make validate       Run local repo validation checks"
	@echo "  make spark-create   Create baseline Iceberg tables"
	@echo "  make spark-quality  Run baseline quality checks"
	@echo "  make trino          Open Trino CLI"

up:
	@export AIRFLOW_UID="$${AIRFLOW_UID:-$$(id -u)}"; \
	if [ -z "$${DOCKER_GID:-}" ]; then \
	  export DOCKER_GID="$$(stat -c '%g' "$(DOCKER_SOCK)" 2>/dev/null || stat -f '%g' "$(DOCKER_SOCK)" 2>/dev/null || echo 999)"; \
	fi; \
	docker compose up -d --build

down:
	docker compose down

ps:
	docker compose ps

logs:
	docker compose logs -f

build:
	docker compose build --no-cache

reset:
	./infra/scripts/reset-poc-data.sh

smoke:
	./infra/scripts/smoke-test.sh

scenarios:
	./scripts/run_all_scenarios.sh

validate:
	python3 scripts/validate_repo_structure.py
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ai-assistant python3 -m unittest discover -s ai-assistant/tests

spark-create:
	docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/01_create_tables.py

spark-quality:
	docker compose exec spark-iceberg spark-submit /home/iceberg/jobs/02_quality_check.py

trino:
	docker compose exec trino trino --server http://localhost:8080 --catalog iceberg --schema gold

superset-shell:
	docker compose exec superset bash

airflow-logs:
	docker compose logs -f airflow
