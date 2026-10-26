.PHONY: install test retest coverage docs lint format


install:
	uv sync --all-groups

test:
	uv run pytest

retest:
	uv run pytest -vvv --lf

coverage:
	uv run coverage run -m pytest
	uv run coverage report

lint:
	uv run ruff format --check src tests
	uv run ruff check src tests

format:
	uv run ruff check --fix src tests
	uv run ruff format src tests

docs:
	uv run --group docs $(MAKE) -C docs html
