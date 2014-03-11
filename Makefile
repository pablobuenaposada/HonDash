PIP=`. venv/bin/activate; which pip`
PYTHON=`. venv/bin/activate; which python`
DEPS:=requirements/requirements.txt
PYTEST=`. venv/bin/activate; which pytest`

clean:
	@rm -rf venv

virtualenv: clean
	@virtualenv venv
	@$(PIP) install -U "pip"
	@$(PIP) install -r $(DEPS)

test: virtualenv
	$(PYTEST)
