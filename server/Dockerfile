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

# Expose port
EXPOSE 3000

# Set environment variables to force IPv4
ENV NODE_OPTIONS="--dns-result-order=ipv4first"
ENV NODE_ENV=development

# Start the application with Node.js ES Module support
CMD ["node", "--experimental-specifier-resolution=node", "src/index.js"]
