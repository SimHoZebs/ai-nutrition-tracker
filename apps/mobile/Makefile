# Makefile for AI Nutrition Tracker
.PHONY: help build up down restart logs migrate makemigrations shell dbshell createsuperuser test clean reset-db

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

# Docker commands
build: ## Build the Docker images
	docker compose build

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

restart: ## Restart all services
	docker compose restart

logs: ## Show logs from all services
	docker compose logs -f

# Django management commands (run in api container)
migrate: ## Run Django migrations
	docker compose exec api python manage.py migrate

makemigrations: ## Create new Django migrations
	docker compose exec api python manage.py makemigrations

shell: ## Open Django shell
	docker compose exec api python manage.py shell

dbshell: ## Open database shell (psql)
	docker compose exec db psql -U nutrition_user -d nutrition_db

createsuperuser: ## Create Django superuser
	docker compose exec api python manage.py createsuperuser

test: ## Run Django tests
	docker compose exec api python manage.py test

reset-db: ## Reset the database by calling the API endpoint
	curl -X POST http://localhost:8000/api/reset-db/

# Utility commands
clean: ## Remove containers, volumes, and images
	docker compose down -v --rmi all

# Database inspection
db-tables: ## List all database tables
	docker compose exec db psql -U nutrition_user -d nutrition_db -c "\dt"

db-inspect: ## Inspect CustomFood table structure
	docker compose exec db psql -U nutrition_user -d nutrition_db -c "\d customfood"