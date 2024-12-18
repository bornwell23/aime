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

# Generate .env file from environment variables
RUN echo "AUTH_SERVICE_SECRET_KEY=${AUTH_SERVICE_SECRET_KEY}" > .env && \
    echo "AUTH_SERVICE_ALGORITHM=${AUTH_SERVICE_ALGORITHM}" >> .env && \
    echo "DATABASE_URL=${DATABASE_URL}" >> .env && \
    echo "ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}" >> .env && \
    echo "LOG_LEVEL=${LOG_LEVEL}" >> .env && \
    echo "LOG_FORMAT=${LOG_FORMAT}" >> .env && \
    echo "PASSWORD_MIN_LENGTH=${PASSWORD_MIN_LENGTH}" >> .env && \
    echo "PASSWORD_REQUIRE_SPECIAL_CHARS=${PASSWORD_REQUIRE_SPECIAL_CHARS}" >> .env && \
    echo "PASSWORD_REQUIRE_NUMBERS=${PASSWORD_REQUIRE_NUMBERS}" >> .env

# Expose the port the app runs on
EXPOSE 8000

# Use environment variable for host
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
