#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for the PostgreSQL database to be available.
# The 'nc' command is now available because of the changes in the Dockerfile.
echo "Waiting for the database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready."

# Apply database migrations.
echo "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Collect all static files into one directory for Nginx.
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Fix permissions so Nginx can read the static and media files.
echo "Fixing file permissions for Nginx..."
chmod -R 755 /home/app/web/staticfiles

echo "Creating super user"
python manage.py createsuperuser --noinput || true
# Execute the main command from the Dockerfile, which in this case
# will be the Gunicorn server command.
echo "Starting the Gunicorn server..."
exec "$@"
