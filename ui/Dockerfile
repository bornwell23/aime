# Build stage
FROM node:20-alpine AS build

# Set working directory
WORKDIR /app

# Copy common folder first
COPY common /app/common

# Copy UI project files
COPY ui /app/ui

# Add a build argument to invalidate cache
ARG BUILD_DATE
RUN echo "Build date: ${BUILD_DATE}"

# Set working directory to the ui to run npm correctly
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

# Copy nginx configuration
COPY ui/nginx/default.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
