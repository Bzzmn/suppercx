include .env
export

.PHONY: install format lint test build run all

install:
	# Install dependencies using Poetry
	poetry install

format:
	# Format code using black
	poetry run black app/ scripts/

lint:
	# Lint code using pylint
	poetry run pylint --disable=R,C,W1203 app/ scripts/

test:
	# Run tests using pytest
	poetry run pytest -vv --cov=app --cov=scripts tests/

build:
	# Build Docker container
	docker build -t suppercx-backend .



run:
	@echo "Running Docker container..."
	@if [ $$(docker ps -a -q -f name=suppercx-backend) ]; then \
		docker rm -f suppercx-backend > /dev/null 2>&1; \
	fi
	@docker run --name suppercx-backend -p 8000:8000 \
		-e POSTGRES_URL \
		-e REDIS_URL \
		-e YOUTUBE_API_KEY \
		-e FIRECRAWL_API_KEY \
		-e OPENAI_API_KEY \
		-e ANTHROPIC_API_KEY \
		-e VOYAGE_API_KEY \
		-e WHATSAPP_API_KEY \
		-e WHATSAPP_VERIFICATION_TOKEN \
		-e WHATSAPP_URL \
		suppercx-backend

migrations:
	# Generate new migrations
	@read -p "Enter migration message: " message; \
	poetry run alembic revision --autogenerate -m "$$message"

migrate:
	# Run database migrations
	poetry run alembic upgrade head

seed:
	# Run seed script
	poetry run python scripts/seed_data.py

dev:
	# Run development server
	poetry run uvicorn app.main:app --reload

# Production environment variables should be set securely and not in the Makefile
run-prod:
	@echo "Running production Docker container..."
	@docker run --name suppercx-backend -p 8000:8000 \
		-e POSTGRES_URL \
		-e REDIS_URL \
		-e YOUTUBE_API_KEY \
		-e FIRECRAWL_API_KEY \
		-e OPENAI_API_KEY \
		-e ANTHROPIC_API_KEY \
		-e VOYAGE_API_KEY \
		-e WHATSAPP_API_KEY \
		-e WHATSAPP_VERIFICATION_TOKEN \
		-e WHATSAPP_URL \
		suppercx-backend



