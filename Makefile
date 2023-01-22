.DEFAULT_GOAL := all
sources = pytest_pretty

.PHONY: install
install:
	pip install -U pip
	pip install -r requirements/all.txt
	pip install -e .
	pre-commit install

.PHONY: refresh-lockfiles
refresh-lockfiles:
	@echo "Updating requirements/*.txt files using pip-compile"
	find requirements/ -name '*.txt' ! -name 'all.txt' -type f -delete
	pip-compile -q --resolver backtracking -o requirements/linting.txt requirements/linting.in
	pip-compile -q --resolver backtracking -o requirements/pyproject.txt pyproject.toml
	pip install --dry-run -r requirements/all.txt

.PHONY: format
format:
	pyupgrade --py37-plus --exit-zero-even-if-changed `find $(sources) -name "*.py" -type f`
	isort $(sources)
	black $(sources)

.PHONY: lint
lint:
	ruff $(sources)
	isort $(sources) --check-only --df
	black $(sources) --check --diff

.PHONY: all
all: lint

.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
