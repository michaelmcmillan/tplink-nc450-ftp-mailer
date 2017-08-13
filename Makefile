# System binaries
SYSTEM_PIP=$(shell which pip3)
SYSTEM_PYTHON=$(shell which python3.6)
SYSTEM_VIRTUALENV=$(shell which virtualenv)

# Project binaries
PIP=$(ENV_DIR)/bin/pip3
PYLINT=$(ENV_DIR)/bin/pylint
PYTHON=$(ENV_DIR)/bin/python3

# Directories
LIB_DIR=./lib
TEST_DIR=./test
SRC_DIR=./src
ENV_DIR=$(LIB_DIR)/env
MODULES=$(SRC_DIR):$(TEST_DIR)

# Flags
TEST_RUNNER=$(PYTHON) -m unittest

# Files
TEST_FILES=test_*.py
REQUIREMENTS=$(LIB_DIR)/requirements.txt

# Environment variables
export PYTHONPATH=$(MODULES)
export PYTHONDONTWRITEBYTECODE=true

install: pip-install
test: unit-test

virtualenv-install:
ifndef SYSTEM_VIRTUALENV
	$(SYSTEM_PIP) install virtualenv
endif
	$(SYSTEM_VIRTUALENV) -p $(SYSTEM_PYTHON) --no-site-packages $(ENV_DIR)

pip-install: virtualenv-install
	@$(PIP) install -r $(REQUIREMENTS)

unit-test:
ifeq (, ${file})
	@$(TEST_RUNNER) discover -s $(TEST_DIR) -p $(TEST_FILES)
else
	@$(TEST_RUNNER) discover -s $(TEST_DIR) -p ${file}
endif

.PHONY: test install
