#!/bin/bash

# Script to start the VK Randomizer Backend on a server using Docker Compose

echo "Starting VK Randomizer Backend services..."

# Start Docker Compose in detached mode
docker compose up --build -d

if [ $? -eq 0 ]; then
    echo "Services started successfully."
    echo "Application is accessible on port 8000."
    echo "Database is accessible on port 5432."
else
    echo "Failed to start services. Check Docker Compose logs for details."
    docker-compose logs
fi
