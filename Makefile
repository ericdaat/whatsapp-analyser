venv: venv/bin/activate


venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/bin/activate


start: venv
	. venv/bin/activate; \
	FLASK_APP="src.application.app.py" \
	FLASK_DEBUG=True \
	flask run;
