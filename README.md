# FastAPI ETL Pipeline

This project provides a simple ETL pipeline using FastAPI, Boto3, Pandas, and DynamoDB.

---

## 📋 Flow

1. Upload a CSV file to the configured S3 bucket.
2. Trigger the ETL process via the `/process-s3-file/` endpoint with the S3 file key.
3. The app will:
   - Extract the file from S3.
   - Transform and clean the data.
   - Load the data into a DynamoDB table.

---

## ⚙️ Requirements

- AWS credentials (via `aws configure`)
- `outputs.json` file generated from the Terraform provisioning
- Python 3.9+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
