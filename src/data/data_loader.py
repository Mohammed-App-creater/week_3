import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(path):
    """
    Loads the ACIS dataset from a pipe-delimited text file.
    
    Args:
        path (str): Absolute path to the dataset file.
        
    Returns:
        pd.DataFrame: Loaded dataframe.
    """
    try:
        logging.info(f"Loading data from {path}...")
        # Read pipe-delimited file
        df = pd.read_csv(path, sep='|', low_memory=False)
        logging.info(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise e

if __name__ == "__main__":
    # Test execution
    test_path = r"C:\Users\yoga\code\10_Academy\week_3\data\raw\MachineLearningRating_v3.txt"
    if os.path.exists(test_path):
        df = load_data(test_path)
        print(df.head())
    else:
        print(f"File not found: {test_path}")
