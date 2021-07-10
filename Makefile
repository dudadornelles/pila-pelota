define VENV
. .venv/bin/activate;PYTHONPATH=$$PYTHONPATH:.
endef

venv:
	test -d .venv || python3 -m venv .venv
	$(VENV) python3 -m pip install --upgrade pip
	$(VENV) pip install -r requirements.txt


clean:
	git clean -dfx

