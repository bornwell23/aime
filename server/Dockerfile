# Use official Node.js LTS image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy server project files
COPY server /app/server

# Copy common folder 
COPY common /app/common

# Add a build argument to invalidate cache
ARG BUILD_DATE
RUN echo "Build date: ${BUILD_DATE}"

# Install dependencies
WORKDIR /app/server
RUN npm ci

# Generate .env file from environment variables
RUN echo "NODE_ENV=${NODE_ENV}" > .env && \
    echo "BACK_PORT=${BACK_PORT}" >> .env && \
    echo "SERVER_LOG_LEVEL=${SERVER_LOG_LEVEL}" >> .env

# Expose port
EXPOSE 3000

# Set environment variables to force IPv4
ENV NODE_OPTIONS="--dns-result-order=ipv4first"
ENV NODE_ENV=development

# Start the application with Node.js ES Module support
CMD ["node", "--experimental-specifier-resolution=node", "src/index.js"]
