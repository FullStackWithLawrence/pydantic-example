SHELL := /bin/bash

ifneq ("$(wildcard .env)","")
    include .env
else
    $(shell echo -e "OPENAI_API_ORGANIZATION=PLEASE-ADD-ME\nOPENAI_API_KEY=PLEASE-ADD-ME\nPINECONE_API_KEY=PLEASE-ADD-ME\nPINECONE_ENVIRONMENT=gcp-starter\nDEBUG_MODE=True\n" >> .env)
endif

.PHONY: analyze init activate lint clean test

# Default target executed when no arguments are given to make.
all: help

analyze:
	cloc . --exclude-ext=svg,json,zip --vcs=git
init:
	npm install && \
	python3.11 -m venv venv && \
	source venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt && \
	pre-commit install

activate:
	. venv/bin/activate

test:
	cd grader && pytest -v -s tests/
	python -m setup_test

lint:
	pre-commit run --all-files && \
	black .

clean:
	rm -rf venv && rm -rf node_modules

release:
	git commit -m "fix: force a new release" --allow-empty && git push

######################
# HELP
######################

help:
	@echo '===================================================================='
	@echo 'analyze             - generate code analysis report'
	@echo 'init            - create a Python virtual environment and install dependencies'
	@echo 'activate        - activate the Python virtual environment'
	@echo 'test            - run Python unit tests'
	@echo 'lint            - run Python linting'
	@echo 'clean           - destroy the Python virtual environment'
