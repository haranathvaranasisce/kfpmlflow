"""Data preparation component for the ML pipeline."""
from kfp import dsl


@dsl.component(
    base_image='python:3.11',
    target_image='gcr.io/my-project/my-component:v1'
)
def dataprep(
    input_data_path: str,
    output_data_path: dsl.OutputPath(str)
) -> str:
    """
    Prepare and preprocess data for training.
    
    Args:
        input_data_path: Path to the input data
        output_data_path: Path to save the processed data
    
    Returns:
        Status message indicating completion
    """
    import pandas as pd
    import json
    
    # Create sample data if input_data_path is empty or doesn't exist
    # This is a placeholder implementation
    try:
        # In a real scenario, you would load data from the input_data_path
        data = {
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [2, 4, 6, 8, 10],
            'target': [0, 1, 0, 1, 0]
        }
        df = pd.DataFrame(data)
        
        # Perform data preprocessing
        # Normalize features
        df['feature1'] = (df['feature1'] - df['feature1'].mean()) / df['feature1'].std()
        df['feature2'] = (df['feature2'] - df['feature2'].mean()) / df['feature2'].std()
        
        # Save processed data
        with open(output_data_path, 'w') as f:
            json.dump(df.to_dict(orient='list'), f)
        
        status = f"Data preparation completed. Processed {len(df)} rows."
        print(status)
        return status
        
    except Exception as e:
        error_msg = f"Error in data preparation: {str(e)}"
        print(error_msg)
        raise
