#!/bin/bash

# Define the path to the .env file for the frontend service
ENV_FILE="frontend/.env"

# Ensure the .env file exists and update its content
echo "Setting up the .env file for the frontend service..."
echo 'VITE_API_URL="http://localhost:8000"' > $ENV_FILE

# Confirm the .env file content
echo "The .env file has been updated with the following content:"
cat $ENV_FILE

# Build and run only the frontend service using Docker Compose
echo "Building and running the frontend service..."

# Build the frontend service
docker-compose build frontend backend postgres pgadmin

# Start the frontend service
docker-compose up -d frontend backend postgres pgadmin

echo "Frontend service is now running!"