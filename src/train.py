"""Model training component for the ML pipeline."""
from kfp import dsl

try:
    from .config import BASE_IMAGE, TARGET_IMAGE
except ImportError:
    from config import BASE_IMAGE, TARGET_IMAGE


@dsl.component(
    base_image=BASE_IMAGE,
    target_image=TARGET_IMAGE
)
def train(
    prepared_data_path: str,
    model_path: dsl.OutputPath(str)
) -> str:
    """
    Train a machine learning model on the prepared data.
    
    Args:
        prepared_data_path: Path to the prepared data
        model_path: Path to save the trained model
    
    Returns:
        Status message with training metrics
    """
    import pandas as pd
    import json
    import pickle
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    
    try:
        # Load prepared data
        with open(prepared_data_path, 'r') as f:
            data_dict = json.load(f)
        
        df = pd.DataFrame(data_dict)
        
        # Split features and target
        X = df[['feature1', 'feature2']]
        y = df['target']
        
        # Split train and test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        model = LogisticRegression(random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = accuracy_score(y_train, model.predict(X_train))
        test_score = accuracy_score(y_test, model.predict(X_test))
        
        # Save model
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        status = (
            f"Model training completed. "
            f"Train accuracy: {train_score:.4f}, "
            f"Test accuracy: {test_score:.4f}"
        )
        print(status)
        return status
        
    except Exception as e:
        error_msg = f"Error in model training: {str(e)}"
        print(error_msg)
        raise
