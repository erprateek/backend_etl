from flask import Flask
import psycopg2
from sqlalchemy import create_engine

app = Flask(__name__)

def etl():
    # Load CSV files
    # Process files to derive features
    # Upload processed data into a database
    '''
    - `users.csv`: Contains user data with the following columns: `user_id`, `name`, `email`,`signup_date`.
    - `user_experiments.csv`: Contains experiment data with the following columns: `experiment_id`, `user_id`, `experiment_compound_ids`, `experiment_run_time`. The `experiment_compound_ids` column contains a semicolon-separated list of compound IDs.
    - `compounds.csv`: Contains compound data with the following columns: `compound_id`, `compound_name`, `compound_structure`.

    ## Feature Derivation
    From the provided CSV files, derive the following features:
    
    1. Total experiments a user ran.
    2. Average experiments amount per user.
    3. User's most commonly experimented compound.
    '''
    users_df             = pd.read_csv(os.path.join('data','users.csv'))
    users_experiments_df = pd.read_csv(os.path.join('data','user_experiments.csv'))
    compounds_df         = pd.read_csv(os.path.join('data','compounds.csv'))

    # 1. Total experiments a user ran.
    total_experiments_per_user = user_experiments_df.groupby('user_id').size().reset_index(name='total_experiments')

    # 2. Average experiments amount per user.
    average_experiments_per_user = user_experiments_df.groupby('user_id').size().mean()

    # 3. User's most commonly experimented compound.
    # Split the experiment_compound_ids and create a new DataFrame to map compounds to experiments
    compound_mapping_df = user_experiments_df.experiment_compound_ids.str.split(';', expand=True).stack().reset_index(level=1, drop=True).to_frame(name='compound_id')
    compound_mapping_df['compound_id'] = compound_mapping_df['compound_id'].astype(int)

    # Merge with the compounds_df to get compound details
    compound_mapping_df = compound_mapping_df.merge(compounds_df, on='compound_id', how='left')
    
    # Count the occurrences of each compound per user and get the most common one for each user
    user_most_common_compound = compound_mapping_df.groupby('user_id')['compound_name'].agg(pd.Series.mode).reset_index()

    # Merge with users_df to include user details
    user_most_common_compound = user_most_common_compound.merge(users_df[['user_id', 'name']], on='user_id', how='left')

    # Rename the columns for clarity
    user_most_common_compound.rename(columns={'compound_name': 'most_common_compound'}, inplace=True)

    # Print the derived features
    print("Total experiments per user:")
    print(total_experiments_per_user)

    print("\nAverage experiments per user:")
    print(average_experiments_per_user)

    print("\nUser's most commonly experimented compound:")
    print(user_most_common_compound)

    # Inject the derived features into the PostgreSQL database
    # Replace these with your PostgreSQL connection details
    POSTGRES_HOST = 'your_host'
    POSTGRES_PORT = 'your_port'
    POSTGRES_DB = 'your_database'
    POSTGRES_USER = 'your_user'
    POSTGRES_PASSWORD = 'your_password'

    # Create a connection to the PostgreSQL database
    conn_str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    engine = create_engine(conn_str)

    # Inject DataFrames into PostgreSQL tables
    total_experiments_per_user.to_sql('total_experiments', engine, if_exists='replace', index=False)
    user_most_common_compound.to_sql('user_most_common_compound', engine, if_exists='replace', index=False)

    # Close the engine connection
    engine.dispose()
    

# Your API that can be called to trigger your ETL process
@app.route('/trigger_etl',methods=['POST'])
def trigger_etl():
    # Trigger your ETL process here
    etl()
    return {"message": "ETL process started"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
