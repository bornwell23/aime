#!/bin/bash
set -e
nginx &
gunicorn --bind 0.0.0.0:4000 --workers 4 "app:create_app()"