#!/bin/bash

# Replace the API endpoint URL with the actual host and port if needed
API_ENDPOINT="http://localhost:5000/trigger_etl"

# Trigger the ETL process using curl (or any other HTTP client)
curl -X POST $API_ENDPOINT
