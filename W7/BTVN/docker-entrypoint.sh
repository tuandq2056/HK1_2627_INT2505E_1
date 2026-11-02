#!/bin/sh
set -e

# Áp migration trước khi nhận traffic
flask db upgrade

exec gunicorn -c gunicorn.conf.py wsgi:app
