usage:
	@echo "usage: make [test]"

test:
	poetry run black git-append
	poetry run flake8 git-append
	poetry run pydocstyle git-append
