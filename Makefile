DEAFULT_GOAL = help
VENV := venv

help:
	@echo "TODO: help info"

# PYTHON COMMANDS
#######################################################################
venv:
	@python3 -m venv $(VENV)

setup: venv
	@. $(VENV)/bin/activate; \
	$(VENV)/bin/pip3 install -e .[dev]

format:
	@black . --exclude './$(VENV)'

build:
	@python3 setup.py sdist bdist_wheel

install: build
	@pip3 install dist/*.whl

clean:
	@rm -rf build; \
		rm -rf dist; \
		rm -rf */*.egg-info; \
		rm -rf *.egg-info; \
		find . -type f -name "*.py[co]" -delete; \
		find . -type d -name "__pycache__" -delete; \
		python3 setup.py clean --all

push:
	@twine upload dist/*