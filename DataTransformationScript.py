import pandas as pd
import numpy as np
from datetime import datetime

def transform_data(cleaned_data):
    """
    Transforms cleaned data by creating new features, 
    encoding categorical variables, and normalizing data.
    """
    df = cleaned_data.copy()
    
    print("Starting data transformation...")
    
    # Create age from birthdate if exists
    if 'birthdate' in df.columns:
        df['birthdate'] = pd.to_datetime(df['birthdate'])
        df['age'] = (datetime.now() - df['birthdate']).dt.days // 365
        df = df.drop('birthdate', axis=1)
    
    # Create full name from first and last name if exists
    if all(col in df.columns for col in ['first_name', 'last_name']):
        df['full_name'] = df['first_name'] + ' ' + df['last_name']
    
    # One-hot encode categorical variables
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        if df[col].nunique() < 10:  # Only encode if reasonable number of categories
            dummies = pd.get_dummies(df[col], prefix=col)
            df = pd.concat([df, dummies], axis=1)
            df = df.drop(col, axis=1)
    
    # Normalize numerical columns (min-max scaling)
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        if df[col].max() - df[col].min() > 0:  # Avoid division by zero
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    
    print("Data transformation completed successfully!")
    return df

if __name__ == "__main__":
    # Example usage
    cleaned_data = pd.read_csv("cleaned_data.csv")
    transformed_data = transform_data(cleaned_data)
    transformed_data.to_csv("transformed_data.csv", index=False)
    print("Transformed data saved to transformed_data.csv")