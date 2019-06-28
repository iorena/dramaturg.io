#!/usr/bin/env bash

export FLASK_APP=web_dramaturgio.server
export FLASK_DEBUG=1
export FLASK_ENV=development
export PYTHONPATH=/home/essalmen/.conda/envs/py3/lib/python3.7/site-packages/syntaxmaker
flask run
