
lint:
	flake8

build:
	rm -rf build dist .mypy_cache GitFx.egg-info
	python3 -m build

release:
	python3 -m twine upload dist/*

release-test:
	python3 -m twine upload --repository testpypi dist/*


.PHONY: lint build release release-test
