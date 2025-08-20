#!/bin/sh
# entrypoint.sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for the PostgreSQL database to be available.
echo "Waiting for the database..."
until PGPASSWORD=$DB_PASSWORD psql -h "db" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
>&2 echo "Postgres is up - continuing..."

# Apply database migrations.
echo "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create a superuser if it doesn't already exist.
# The --noinput flag requires a username and email to be passed.
echo "Checking for a superuser..."
if [ -z "$DJANGO_SUPERUSER_USERNAME" ] || [ -z "$DJANGO_SUPERUSER_EMAIL" ] || [ -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD must be set to create a superuser."
else
  python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists(): User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')"
fi

# Collect all static files into one directory for Nginx.
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Fix permissions so Nginx can read the static and media files.
echo "Fixing file permissions for Nginx..."
chmod -R 755 /home/app/web/staticfiles

echo "Starting the Gunicorn server..."
exec "$@"
