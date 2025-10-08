#!/bin/bash
# migrate.sh


# 1. Запуск миграций Alembic
alembic upgrade head

# 2. Запуск основного приложения
exec python3 -m src.main
