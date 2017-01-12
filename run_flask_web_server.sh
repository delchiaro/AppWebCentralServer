. venv/bin/activate
export FLASK_APP=./www_web/index.py
export FLASK_DEBUG=1
venv/bin/flask run --host=0.0.0.0 --port=5000

deactivate
