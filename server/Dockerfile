# Use official Node.js LTS image
FROM node:20-alpine

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

# Set environment variables to force IPv4
ENV NODE_OPTIONS="--dns-result-order=ipv4first"
ENV NODE_ENV=development

# Start the application with Node.js ES Module support
CMD ["node", "--experimental-specifier-resolution=node", "src/index.js"]
