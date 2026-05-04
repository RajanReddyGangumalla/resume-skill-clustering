"""
Preprocessing module for cleaning and preparing resume data.
"""

import pandas as pd
import numpy as np
import re
import string


def load_dataset(file_path):
    """Load the dataset from CSV file."""
    try:
        df = pd.read_csv(file_path)
        print(f"Dataset loaded successfully: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        raise


def identify_resume_column(df):
    """Identify which column contains resume text."""
    # Common column names for resume text
    possible_columns = ['Resume_str', 'Resume_html', 'resume', 'Resume', 'text', 'content', 'description']
    
    for col in possible_columns:
        if col in df.columns:
            print(f"Identified resume column: {col}")
            return col
    
    # If no common column found, try to find the column with most text
    text_columns = df.select_dtypes(include=['object']).columns
    if len(text_columns) > 0:
        # Find column with longest average text length
        max_length = 0
        best_col = text_columns[0]
        
        for col in text_columns:
            avg_length = df[col].astype(str).str.len().mean()
            if avg_length > max_length:
                max_length = avg_length
                best_col = col
        
        print(f"Identified resume column by text length: {best_col}")
        return best_col
    
    raise ValueError("Could not identify resume text column in the dataset")


def clean_text(text):
    """Clean and normalize text data."""
    if not isinstance(text, str):
        text = str(text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+', ' ', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', ' ', text)
    
    # Remove phone numbers
    text = re.sub(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', ' ', text)
    
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def remove_stopwords(text):
    """Remove common stopwords from text."""
    # Common English stopwords
    stopwords = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
        'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
        'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
        'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
        'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
        'by', 'for', 'with', 'through', 'during', 'before', 'after', 'above', 'below',
        'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
        'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
        'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
        'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
        'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn',
        'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn'
    }
    
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords]
    return ' '.join(filtered_words)


def preprocess_resumes(df, resume_column):
    """Preprocess the resume data."""
    print("Preprocessing resume data...")
    
    # Create a copy to avoid modifying original dataframe
    df_processed = df.copy()
    
    # Clean the resume text
    print("Cleaning resume text...")
    df_processed['cleaned_resume'] = df_processed[resume_column].apply(clean_text)
    
    # Remove stopwords
    print("Removing stopwords...")
    df_processed['cleaned_resume'] = df_processed['cleaned_resume'].apply(remove_stopwords)
    
    # Remove empty resumes
    initial_count = len(df_processed)
    df_processed = df_processed[df_processed['cleaned_resume'].str.len() > 10]
    final_count = len(df_processed)
    
    print(f"Removed {initial_count - final_count} empty or very short resumes")
    print(f"Preprocessing completed: {final_count} resumes processed")
    
    return df_processed


def print_dataset_info(df):
    """Print basic information about the dataset."""
    print("\n" + "="*50)
    print("DATASET INFORMATION")
    print("="*50)
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Data types:\n{df.dtypes}")
    print(f"Missing values:\n{df.isnull().sum()}")
    print("="*50)
