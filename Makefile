usage:
	@echo "usage: make [test]"

format:
	poetry run black src/

lint:
	poetry run flake8 src/
	poetry run pydocstyle src/

test:
	poetry run pytest tests/

install:
	poetry install --with=dev
