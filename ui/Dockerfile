FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ui/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir flake8 pylint

# Copy application code
COPY ui/src/ .
COPY common /app/common

# Run syntax checks
RUN echo "Running syntax checks..." && python -m compileall .
RUN echo "Running flake8..." && flake8 --ignore=W293,E501,F841 .
RUN echo "Running pylint..." && pylint --disable=C,R,W --enable=E --ignore=tests .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose ports
EXPOSE 3000

# Start Nginx and Gunicorn
CMD ["python", "app.py"]
