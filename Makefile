format:
	black .
	isort .

lint:
	ruff check .

check:
	black --check .
	isort --check-only .
	ruff check .

fix:
	black .
	isort .
	ruff check --fix .