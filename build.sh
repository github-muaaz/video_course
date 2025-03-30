#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py createsuperuser --noinput || true

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"
