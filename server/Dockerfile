FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ .

# Make entrypoint script executable
COPY src/entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create static directory
RUN mkdir -p /app/static

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py

# Expose ports
EXPOSE 80

# Start Nginx and Gunicorn
ENTRYPOINT ["/app/entrypoint.sh"]
