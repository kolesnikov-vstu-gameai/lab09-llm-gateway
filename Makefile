# Единая точка входа в проект. Список целей: make help
# Windows: установите make (choco install make) или выполняйте команды из целей вручную.
.DEFAULT_GOAL := help
PYTHON ?= python

.PHONY: help install env precommit run loadtest lint format test check up down clean

# ---------- Установка ----------
install: ## Установить зависимости (pip install -r requirements.txt)
	$(PYTHON) -m pip install -r requirements.txt

env: ## Создать .env из .env.example (если ещё нет)
	cp -n .env.example .env

precommit: ## Установить git-хуки pre-commit
	pre-commit install

# ---------- Запуск ----------
run: ## Запустить gateway локально (нужен Redis: make up или redis-server)
	uvicorn gateway.app:app --reload

loadtest: ## Нагрузочный тест locust против http://localhost:8000
	locust -f loadtest/locustfile.py --host http://localhost:8000

# ---------- Проверка ----------
lint: ## Проверить код линтером ruff
	ruff check .

format: ## Отформатировать код и применить автоисправления ruff
	ruff format . && ruff check --fix .

test: ## Запустить тесты pytest
	pytest

check: lint test ## Линтер + тесты (то же, что CI)

# ---------- Docker ----------
up: ## Поднять gateway + redis в Docker Compose
	docker compose up --build

down: ## Остановить контейнеры
	docker compose down

# ---------- Обслуживание ----------
clean: ## Удалить кеши Python, pytest, ruff и egg-info
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .ruff_cache -o -name '*.egg-info' \) -prune -exec rm -rf {} +

help: ## Показать список целей
	@grep -hE '^[a-zA-Z0-9_-]+:.*## ' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

