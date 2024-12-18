#!/bin/bash

# Define the path to the .env file for the frontend service
ENV_FILE="frontend/.env"

# Update the .env file with the required content
echo "Updating the .env file for the frontend service..."
cat > $ENV_FILE <<EOL
VITE_API_URL="http://backend:8000"
PLAYWRIGHT_URL="http://frontend:80"
PLAYWRIGHT_BACKEND_URL="http://backend:8000"
EOL

# Confirm the .env file content
echo "The .env file has been updated with the following content:"
cat $ENV_FILE

# Build all services using Docker Compose
echo "Building all services..."
docker-compose build

# Start all services
echo "Starting all services..."
docker-compose up -d

echo "All services are now running!"