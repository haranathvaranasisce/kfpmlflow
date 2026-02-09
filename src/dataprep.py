"""Data preparation component for the ML pipeline."""
from kfp import dsl

try:
    from .config import BASE_IMAGE, TARGET_IMAGE
    from .common.util import print_module_name
except ImportError:
    from config import BASE_IMAGE, TARGET_IMAGE
    from common.util import print_module_name


@dsl.component(
    base_image=BASE_IMAGE,
    target_image=TARGET_IMAGE
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
    
    # Print module name using common utility
    print_module_name()
    
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
        # Normalize features using safe normalization (handles zero std)
        for col in ['feature1', 'feature2']:
            mean = df[col].mean()
            std = df[col].std()
            if std > 0:
                df[col] = (df[col] - mean) / std
            else:
                df[col] = df[col] - mean  # Only center if std is zero
        
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
