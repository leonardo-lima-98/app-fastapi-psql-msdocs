#!/bin/bash
set -e
python3 -m pip install --upgrade pip
python3 -m pip install -e src
python3 src/fastapi_app/seed_data.py
python3 -m gunicorn src.fastapi_app:app
