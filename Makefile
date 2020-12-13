.PHONY: dist docs

export PIPENV_VERBOSITY = -1

format ?= html

docs: docs-build

dist: dist-build
	twine check dist/*
	twine upload --skip-existing dist/*

dist-clean:
	[ -f dist/*.whl ] && mkdir -p wheels && mv dist/*.whl wheels || true
	[ -f dist/*.tar.gz ] && mkdir -p sdist && mv dist/*.tar.gz sdist || true
	[ -f dist/*.egg ] && mkdir -p eggs && mv dist/*.egg eggs || true

dist-build: dist-clean
	pipenv run python setup.py sdist bdist_wheel

docs-build:
	pipenv run $(MAKE) -C docs ${format}

docs-api:
	pipenv run sphinx-apidoc -e -P -M --no-headings -o docs/source flask_datatables

isort:
	pipenv run isort -l100 --color flask_datatabless
