#!/bin/bash
# migrate.sh

# Настройки подключения к БД
HOST=$DB_HOST
PORT=$DB_PORT

# Ожидание готовности базы данных
echo "Waiting for PostgreSQL ($HOST:$PORT) to be ready..."

# Цикл ожидания: повторять до тех пор, пока не будет установлена связь
until nc -z $HOST $PORT; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing command"

# 1. Запуск миграций Alembic
alembic upgrade head

# 2. Запуск основного приложения
exec python3 -m src.main