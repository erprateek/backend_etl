#!/bin/bash

# Connect to the PostgreSQL database and execute a query to showcase data

# Replace the following variables with your PostgreSQL connection details
POSTGRES_HOST="my_db_host"
POSTGRES_PORT="5432"
POSTGRES_DB="mydatabase"
POSTGRES_USER="myuser"
POSTGRES_PASSWORD="mypassword"

# Query to showcase the data from the database
QUERY="SELECT * FROM your_table;"

# Connect and execute the query using psql
docker run -it --rm \
  -e PGPASSWORD=$POSTGRES_PASSWORD \
  postgres:latest psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -c "$QUERY"
