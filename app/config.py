import json

# Load outputs from Terraform's static file
with open('outputs.json') as f:
    outputs = json.load(f)

# Settings
S3_BUCKET_NAME = outputs["bucket_name"]["value"]
DYNAMODB_TABLE_NAME = outputs["table_name"]["value"]
AWS_REGION = outputs["region"]["value"]
