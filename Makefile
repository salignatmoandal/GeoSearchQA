# Makefile

.PHONY: setup run clean lint docker-build docker-run docker-stop

# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Installation et configuration
setup:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Exécution en local
run:
	$(PYTHON) -m app.main

# Nettoyage
clean:
	rm -rf __pycache__
	rm -rf app/__pycache__
	rm -rf app/*/__pycache__

# Linting
lint:
	$(PYTHON) -m flake8 app

# Docker
docker-build:
	docker compose up --build

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f