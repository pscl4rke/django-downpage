
pre-release-checks:
	pyroma .

test: | venv.testing
	venv.testing/bin/coverage run -m unittest discover tests/
	venv.testing/bin/coverage report -m

venv.testing:
	python3 -m venv $@
	$@/bin/pip install -e '.[testing]'

release: export PYTHON_KEYRING_BACKEND := keyring.backends.null.Keyring
release:
	test '$(shell python3 setup.py --version)' = '$(shell git describe --tags)'
	test ! -d dist
	python3 setup.py sdist bdist_wheel
	check-wheel-contents dist
	twine check dist/*
	twine upload dist/*
	mv -i build* *.egg-info dist/.
	mv dist dist.$$(date +%Y-%m-%d.%H%M%S)
