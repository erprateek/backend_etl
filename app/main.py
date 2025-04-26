from fastapi import FastAPI
from app.etl.extractor import extract_all_data
from app.etl.transformer import transform_data
from app.etl.loader import load_to_dynamodb

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ETL Pipeline is Ready"}

@app.post("/run-etl/")
async def run_etl():
    """
    End-to-end ETL pipeline execution.
    """
    users_df, experiments_df, compounds_df = extract_all_data()
    final_df, avg_experiments = transform_data(users_df, experiments_df, compounds_df)
    load_to_dynamodb(final_df)
    
    return {
        "status": "success",
        "total_users_processed": len(final_df),
        "average_experiments_per_user": avg_experiments
    }
