. venv/bin/activate
export FLASK_APP=./www_link/index.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=5002

deactivate
