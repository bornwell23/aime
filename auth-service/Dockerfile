# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Add a build argument to invalidate cache
ARG BUILD_DATE
RUN echo "Build date: ${BUILD_DATE}"

# Copy auth-service project files
COPY auth-service/ /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc postgresql-client \
    && rm -rf /var/lib/apt/lists/*

#Install Python dependencies

RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Use environment variable for host
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
