import boto3
from app.config import DYNAMODB_TABLE_NAME, AWS_REGION

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def load_to_dynamodb(df):
    """
    Load processed user data into DynamoDB.
    """
    with table.batch_writer() as batch:
        for _, row in df.iterrows():
            item = {
                "user_id": str(row["user_id"]),
                "name": row["name"],
                "email": row["email"],
                "signup_date": str(row["signup_date"]),
                "total_experiments": int(row["total_experiments"]),
                "top_compound_id": str(row["top_compound_id"]),
                "top_compound_name": row["compound_name"]
            }
            batch.put_item(Item=item)
