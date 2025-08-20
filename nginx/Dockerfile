# Use the official Nginx image as the base
FROM nginx:1.25-alpine

# Remove the default Nginx configuration file to ensure ours is used
RUN rm /etc/nginx/conf.d/default.conf

# Copy your custom configuration file into the container
COPY ./django_app.conf /etc/nginx/conf.d/django_app.conf

# Expose port 80 to the host (already handled by docker-compose)
EXPOSE 80

