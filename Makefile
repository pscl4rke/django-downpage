
release:
	test ! -d dist
	python3 setup.py sdist bdist_wheel
	ls -la dist
	PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring twine upload dist/*
	mv -i build* *.egg-info dist/.
	mv dist dist.$$(date +%Y%m%d.%H%M%S)
