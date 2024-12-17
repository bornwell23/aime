# Use official Node.js LTS image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Set working directory to server
WORKDIR /app/server

# Install dependencies
RUN npm ci

# Expose port
EXPOSE 3000

# Start the application with Node.js ES Module support
CMD ["node", "--experimental-specifier-resolution=node", "src/index.js"]
