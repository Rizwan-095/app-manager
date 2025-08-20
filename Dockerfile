# Start from the official Python image
FROM python:3.11.4-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /home/app/web

# Install system dependencies
# Install the 'netcat-openbsd' package to provide the 'nc' command
RUN apt-get update && apt-get install -y --no-install-recommends \
  netcat-openbsd \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script
COPY ./entrypoint.sh /home/app/web/entrypoint.sh

# Copy the entire project code
COPY . .

# Grant execute permissions to the entrypoint script
RUN chmod +x /home/app/web/entrypoint.sh

# Expose the port Gunicorn will run on
EXPOSE 8000

# Set the entrypoint for the container
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
