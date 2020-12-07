.PHONY: dist

export PIPENV_VERBOSITY = -1

isort:
	pipenv run isort -l100 --color flask_datatables

dist-clean:
	[ -f dist/*.whl ] && mkdir -p wheels && mv dist/*.whl wheels || true
	[ -f dist/*.tar.gz ] && mkdir -p sdist && mv dist/*.tar.gz sdist || true
	[ -f dist/*.egg ] && mkdir -p eggs && mv dist/*.egg eggs || true

dist-build: dist-clean
	pipenv run python setup.py sdist bdist_wheel

dist:
	twine check dist/*
	twine upload --skip-existing dist/*
