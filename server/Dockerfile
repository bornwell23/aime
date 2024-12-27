FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir flake8 pylint

# Run syntax checks
RUN echo "Running syntax checks..." && python -m compileall .
RUN echo "Running flake8..." && flake8 --ignore=W293,E501,F841 .
RUN echo "Running pylint..." && pylint --disable=C,R,W --enable=E --ignore=tests .

# Copy application code
COPY server/src/ .
COPY common /app/common

# Make entrypoint script executable
COPY server/src/entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Copy Nginx configuration
COPY server/nginx.conf /etc/nginx/nginx.conf

# Create static directory
RUN mkdir -p /app/static

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py

# Expose ports
EXPOSE 80

# Start Nginx and Gunicorn
ENTRYPOINT ["/app/entrypoint.sh"]
