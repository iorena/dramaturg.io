#!/usr/bin/env bash

export FLASK_APP=web_dramaturgio.server
export FLASK_DEBUG=1
export FLASK_ENV=development
export PYTHONPATH=/home/vrsaari/Documents/projects/dramaturgio/venv/lib/python3.6/site-packages/syntaxmaker
flask run
