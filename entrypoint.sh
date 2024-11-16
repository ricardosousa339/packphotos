#!/bin/sh

# Execute as migrações do banco de dados
poetry run alembic upgrade head

# Inicie o aplicativo
exec poetry run uvicorn fast_zero.app:app --host 0.0.0.0 --port 8000