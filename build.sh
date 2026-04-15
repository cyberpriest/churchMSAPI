#!/usr/bin/env bash
set -o errexit

pip install -r backend/requirements.txt

cd backend
python -m alembic upgrade head