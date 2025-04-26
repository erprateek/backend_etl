import boto3
import pandas as pd
from app.config import S3_BUCKET_NAME, AWS_REGION

s3_client = boto3.client('s3', region_name=AWS_REGION)

def extract_csv_from_s3(file_key: str) -> pd.DataFrame:
    """
    Extract CSV file from S3 and load into a pandas DataFrame.
    """
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_key)
    df = pd.read_csv(response['Body'])
    return df

def extract_all_data():
    """
    Extract all required datasets from S3.
    """
    users_df = extract_csv_from_s3('data/users.csv')
    experiments_df = extract_csv_from_s3('data/user_experiments.csv')
    compounds_df = extract_csv_from_s3('data/compounds.csv')
    return users_df, experiments_df, compounds_df
