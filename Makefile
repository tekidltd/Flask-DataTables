export PIPENV_VERBOSITY = -1

isort:
	pipenv run isort -l100 --color flask_datatables
