# reference
# 2018 aws s3 sync --no-sign-request --region eu-west-3  "s3://cse-cic-ids2018/" data &> out &
# 2017 wget --no-parent --recursive "https://iscxdownloads.cs.unb.ca/iscxdownloads/CIC-IDS-2017/" &> out &

DATASET =

PYTHON_ENV = .env
PYTHON_ENV_BIN = $(PYTHON_ENV)/bin
PYTHON = $(PYTHON_ENV_BIN)/python

$(PYTHON_ENV):
	python3 -m venv $@

init: requirements.txt $(PYTHON_ENV)
	$(PYTHON_ENV_BIN)/pip install -r $<

test:
	$(PYTHON) -m unittest
