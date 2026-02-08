"""Data preparation component for KFP V2 pipeline."""

from typing import NamedTuple


def dataprep_component() -> NamedTuple('DataprepOutputs', [('train_data', str), ('test_data', str)]):
    """
    Data preparation component that outputs train and test datasets.
    
    Returns:
        NamedTuple containing paths to train and test datasets
    """
    from common.utils import check
    from collections import namedtuple
    import pandas as pd
    import os
    
    # Call check function from commons
    check("dataprep")
    
    # Create sample data
    print("Preparing training and test datasets...")
    
    # Create sample train data
    train_df = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [2, 4, 6, 8, 10],
        'target': [0, 1, 0, 1, 0]
    })
    
    # Create sample test data
    test_df = pd.DataFrame({
        'feature1': [6, 7, 8],
        'feature2': [12, 14, 16],
        'target': [1, 0, 1]
    })
    
    # Save datasets
    os.makedirs('/tmp/data', exist_ok=True)
    train_path = '/tmp/data/train.csv'
    test_path = '/tmp/data/test.csv'
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f"Train data saved to: {train_path}")
    print(f"Test data saved to: {test_path}")
    
    # Return outputs
    DataprepOutputs = namedtuple('DataprepOutputs', ['train_data', 'test_data'])
    return DataprepOutputs(train_path, test_path)
