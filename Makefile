.PHONY: init tensorboard kill-tensorboard clean-files

ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

## Create virtual environment and install dependencies
init:
	python3.13 -m pip install --no-cache-dir -U pip "poetry>=2.0.0" && \
	poetry config virtualenvs.in-project true && \
	poetry config virtualenvs.create true && \
	poetry config virtualenvs.path .venv && \
	poetry install --no-cache


## Run experiments
run:
	poetry run python src/experimentation/run_uci_datasets_experiment.py

DEFAULT_GOAL := help
.PHONY: help
help:
	@echo "\n$$(tput bold)Available rules:$$(tput sgr0)\n"
	@awk '/^##/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t
