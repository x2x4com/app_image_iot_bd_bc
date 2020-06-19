#!/bin/bash
export FLASK_ENV=production


gunicorn --limit-request-line 0 --limit-request-field_size 0 --limit-request-fields 10000 -c gunicorn.cfg.py main:app
