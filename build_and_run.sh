#!/bin/bash

# Build the Docker image
docker build -t my_python_api .

# Run the Docker container, exposing port 5000
docker run -d -p 5000:5000 \
  -e POSTGRES_HOST=my_db_host \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_DB=mydatabase \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  --name my_python_api_container my_python_api
