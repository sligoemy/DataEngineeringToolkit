import pandas as pd
import numpy as np
import re

def clean_data(input_file):
    """
    Cleans data from an Excel file by handling missing values,
    standardizing formats, and removing duplicates.
    """
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    print(f"Original data shape: {df.shape}")
    
    # Remove duplicate rows
    df = df.drop_duplicates()
    print(f"After removing duplicates: {df.shape}")
    
    # Standardize text columns (remove extra spaces and convert to proper case)
    text_columns = df.select_dtypes(include=['object']).columns
    for col in text_columns:
        df[col] = df[col].astype(str).str.strip().str.title()
    
    # Handle missing values
    # For numeric columns, fill with median
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        df[col] = df[col].fillna(df[col].median())
    
    # For categorical columns, fill with mode
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown")
    
    # Clean email format if exists
    if 'email' in df.columns:
        df['email'] = df['email'].str.lower()
    
    # Clean phone numbers if exists
    if 'phone' in df.columns:
        df['phone'] = df['phone'].astype(str).apply(lambda x: re.sub(r'\D', '', x))
    
    print("Data cleaning completed successfully!")
    return df

if __name__ == "__main__":
    # Example usage
    cleaned_data = clean_data("source_data.xlsx")
    cleaned_data.to_csv("cleaned_data.csv", index=False)
    print("Cleaned data saved to cleaned_data.csv")