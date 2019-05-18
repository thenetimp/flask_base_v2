#!/bin/sh

export FLASK_APP="test_app.py"
flask db upgrade

python -m unittest app/tests/tests_models.py
