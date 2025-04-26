#!/bin/bash

# Read the outputs from the static JSON file
# This assumes you have a file named outputs.json in the same directory
# containing the outputs from your Terraform deployment
if [ ! -f outputs.json ]; then
  echo "Error: outputs.json file not found!"
  exit 1
fi
# Extract the necessary values from the JSON file
EC2_PUBLIC_IP=$(jq -r .ec2_public_ip.value outputs.json)
EC2_PRIVATE_IP=$(jq -r .ec2_private_ip.value outputs.json)
BUCKET_NAME=$(jq -r .bucket_name.value outputs.json)

# SSH into the EC2 instance and deploy the FastAPI app
ssh -o StrictHostKeyChecking=no ec2-user@$EC2_PUBLIC_IP << EOF
  # Navigate to the app directory
  cd /path/to/your/app

  # Pull the latest code
  git pull origin main

  # Restart the app (e.g., using Docker)
  docker-compose up -d
EOF

# You can also use $BUCKET_NAME to interact with the S3 bucket if needed
echo "Deployed app to EC2 instance with public IP: $EC2_PUBLIC_IP"
