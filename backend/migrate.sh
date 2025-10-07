set -e

echo "🔄 Starting Alembic migrations..."

alembic upgrade head
echo "✅ Alembic migrations completed."
exec "$@"