.PHONY: help install run test test-cov lint db-init db-migrate db-upgrade db-reset clean

help:
	@echo "Fyyur Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install Python dependencies"
	@echo ""
	@echo "Running:"
	@echo "  make run              Start the Flask application"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run unit tests"
	@echo "  make test-cov         Run tests with coverage report (HTML)"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             Run flake8 linter"
	@echo ""
	@echo "Database:"
	@echo "  make db-init          Initialize database (create tables)"
	@echo "  make db-migrate       Create a new database migration"
	@echo "  make db-upgrade       Apply pending migrations"
	@echo "  make db-reset         Reset database (drop and recreate all tables)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove generated files and caches"

install:
	pip install -r requirements.txt

run:
	python app.py

test:
	python -m pytest tests/ -v

test-cov:
	python -m pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing
	@echo ""
	@echo "Coverage report generated! Open htmlcov/index.html to view"

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

db-init:
	python -c "from app import db, app; app.app_context().push(); db.create_all(); print('Database initialized!')"

db-migrate:
	flask db migrate

db-upgrade:
	flask db upgrade

db-reset:
	python -c "from app import db, app; app.app_context().push(); db.drop_all(); db.create_all(); print('Database reset!')"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	@echo "Cleanup complete!"
