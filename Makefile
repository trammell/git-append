usage:
	@echo "usage: make [test]"

format:
	poetry run black src/ tests/

lint:
	poetry check
	poetry run flake8 src/ tests/
	poetry run pydocstyle src/ tests/
	poetry run mypy src/ tests/
	poetry run bandit --quiet -c pyproject.toml -r src/

test:
	poetry run coverage run -m pytest -vvv

install:
	poetry install --sync --with=dev --no-root

help:
	poetry run git-append --help
