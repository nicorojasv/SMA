#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Create static directory if it doesn't exist
mkdir -p static

# Convert static asset files
python SMA/manage.py collectstatic --no-input --clear

# Apply any outstanding database migrations
python SMA/manage.py migrate

# Start the application with Gunicorn
# cd SMA && python -m gunicorn SMA.asgi:application -k uvicorn.workers.UvicornWorker