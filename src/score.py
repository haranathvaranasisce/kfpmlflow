"""Model scoring component for the ML pipeline."""
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
def score(
    model_path: str,
    prepared_data_path: str,
    predictions_path: dsl.OutputPath(str)
) -> str:
    """
    Score/evaluate the trained model on data.
    
    Args:
        model_path: Path to the trained model
        prepared_data_path: Path to the data for scoring
        predictions_path: Path to save the predictions
    
    Returns:
        Status message with scoring results
    """
    import pandas as pd
    import json
    import pickle
    from sklearn.metrics import accuracy_score, classification_report
    
    # Print module name using common utility
    print_module_name()
    
    try:
        # Load model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        # Load data
        with open(prepared_data_path, 'r') as f:
            data_dict = json.load(f)
        
        df = pd.DataFrame(data_dict)
        
        # Split features and target
        X = df[['feature1', 'feature2']]
        y = df['target']
        
        # Make predictions
        predictions = model.predict(X)
        probabilities = model.predict_proba(X)
        
        # Calculate metrics
        accuracy = accuracy_score(y, predictions)
        
        # Save predictions
        results = {
            'predictions': predictions.tolist(),
            'probabilities': probabilities.tolist(),
            'actual': y.tolist(),
            'accuracy': accuracy
        }
        
        with open(predictions_path, 'w') as f:
            json.dump(results, f)
        
        status = (
            f"Model scoring completed. "
            f"Accuracy: {accuracy:.4f}, "
            f"Total predictions: {len(predictions)}"
        )
        print(status)
        return status
        
    except Exception as e:
        error_msg = f"Error in model scoring: {str(e)}"
        print(error_msg)
        raise
