
test: | test-venv
	./test-venv/bin/coverage run --source=downpage -m unittest discover ./tests
	./test-venv/bin/coverage report -m

test-venv:
	python3 -m venv $@
	$@/bin/pip install -e '.[testing]'

release:
	test ! -d dist
	python3 setup.py sdist bdist_wheel
	ls -la dist
	PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring twine upload dist/*
	mv -i build* *.egg-info dist/.
	mv dist dist.$$(date +%Y%m%d.%H%M%S)
