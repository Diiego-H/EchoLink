#!/bin/bash

# Stop all running containers
echo "Stopping all running containers..."
docker stop $(docker ps -q)

# Remove all containers (stopped and running)
echo "Removing all containers..."
docker rm -f $(docker ps -aq)

# Remove all images
echo "Removing all images..."
docker rmi -f $(docker images -q)

# Remove all volumes
echo "Removing all volumes..."
docker volume rm $(docker volume ls -q)

# Remove all networks (except default ones)
echo "Removing all networks..."
docker network prune -f

# Clean up any remaining system cache
echo "Cleaning up Docker system cache..."
docker system prune -a -f --volumes

echo "Docker cleanup complete!"