#!/bin/bash
set -e

echo "▶ Running Django migrations..."
python3 manage.py makemigrations || echo "No changes to migrate"
python3 manage.py migrate

echo "▶ Starting Django server..."
python3 manage.py runserver 0.0.0.0:8010
