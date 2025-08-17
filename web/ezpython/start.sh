#!/bin/bash

echo "$FLAG" > /flag
chmod 600 /flag
unset FLAG

export FLASK_APP=app.py
export FLASK_ENV=production

flask run --host=0.0.0.0 --port=5000