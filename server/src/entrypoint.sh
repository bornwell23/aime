#!/bin/bash
set -e

# Wait 5 seconds for postgres and auth-service to start
sleep 5

# Initialize database
python database.py

# Start Nginx
nginx &

# Start Gunicorn
gunicorn --bind 0.0.0.0:4000 --workers 4 "app:create_app()"