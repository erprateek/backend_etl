import pandas as pd

def transform_data(users_df: pd.DataFrame, experiments_df: pd.DataFrame, compounds_df: pd.DataFrame):
    """
    Perform ETL transformations to derive user metrics.
    """
    # Explode experiment_compound_ids into rows
    experiments_df['experiment_compound_ids'] = experiments_df['experiment_compound_ids'].str.split(';')
    experiments_exploded = experiments_df.explode('experiment_compound_ids')
    
    # Total experiments per user
    total_experiments = experiments_df.groupby('user_id').size().reset_index(name='total_experiments')
    
    # Average experiments per user (single number)
    avg_experiments = total_experiments['total_experiments'].mean()
    
    # Most commonly experimented compound per user
    most_common_compound = experiments_exploded.groupby(['user_id', 'experiment_compound_ids']) \
                                               .size() \
                                               .reset_index(name='count')
    
    idx = most_common_compound.groupby('user_id')['count'].idxmax()
    user_top_compound = most_common_compound.loc[idx, ['user_id', 'experiment_compound_ids']]
    user_top_compound = user_top_compound.rename(columns={'experiment_compound_ids': 'top_compound_id'})

    # Merge user info
    final_df = users_df.merge(total_experiments, on='user_id', how='left')
    final_df = final_df.merge(user_top_compound, on='user_id', how='left')
    
    # Join compound name
    final_df = final_df.merge(compounds_df[['compound_id', 'compound_name']], 
                              left_on='top_compound_id', right_on='compound_id', how='left')
    final_df = final_df.drop(columns=['compound_id'])
    
    return final_df, avg_experiments
