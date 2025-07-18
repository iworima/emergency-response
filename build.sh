#!/usr/bin/env bash

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python src/manage.py migrate

# Collect static files (for Django admin)
python src/manage.py collectstatic --noinput
