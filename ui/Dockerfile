# Test stage for syntax checking
FROM python:3.11-slim AS test

WORKDIR /app

# Install dependencies including syntax checkers
COPY ui/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir flake8 pylint

# Copy application code
COPY ui/src/ .
COPY common /app/common

# Set Python path for imports
ENV PYTHONPATH=/app

# Run syntax checks
RUN echo "Running syntax checks..." && python -m compileall .
RUN echo "Running flake8..." && flake8 --ignore=W293,E501,F841 .
RUN echo "Running pylint..." && pylint --disable=C,R,W --enable=E --ignore=tests ./*.py

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY ui/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ui/src/ .
COPY common /app/common

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Expose port
EXPOSE 3000

# Run the application
CMD ["python", "app.py"]
