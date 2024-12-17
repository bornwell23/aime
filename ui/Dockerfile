# Build stage
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Set working directory to ui
WORKDIR /app/ui

# Install dependencies
RUN npm ci

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/ui/dist /usr/share/nginx/html

# Copy common directory to production stage
COPY --from=build /app/common /app/common

# Copy custom nginx configuration
COPY ui/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
