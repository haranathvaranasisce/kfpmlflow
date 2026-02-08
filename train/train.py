"""Training component for KFP V2 pipeline."""

from typing import NamedTuple


def train_component(train_data: str) -> NamedTuple('TrainOutputs', [('model', str), ('metrics', str)]):
    """
    Training component that takes train dataset and outputs metrics and model.
    
    Args:
        train_data: Path to training dataset
        
    Returns:
        NamedTuple containing paths to model and metrics
    """
    from common.utils import check
    from collections import namedtuple
    import pandas as pd
    import json
    import os
    import pickle
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    
    # Call check function from commons
    check("train")
    
    print(f"Loading training data from: {train_data}")
    
    # Load training data
    train_df = pd.read_csv(train_data)
    
    # Prepare features and target
    X_train = train_df[['feature1', 'feature2']]
    y_train = train_df['target']
    
    # Train model
    print("Training logistic regression model...")
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Calculate metrics
    y_pred = model.predict(X_train)
    metrics = {
        'accuracy': float(accuracy_score(y_train, y_pred)),
        'precision': float(precision_score(y_train, y_pred, zero_division=0)),
        'recall': float(recall_score(y_train, y_pred, zero_division=0))
    }
    
    print(f"Training metrics: {metrics}")
    
    # Save model and metrics
    os.makedirs('/tmp/models', exist_ok=True)
    model_path = '/tmp/models/model.pkl'
    metrics_path = '/tmp/models/metrics.json'
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"Model saved to: {model_path}")
    print(f"Metrics saved to: {metrics_path}")
    
    # Return outputs
    TrainOutputs = namedtuple('TrainOutputs', ['model', 'metrics'])
    return TrainOutputs(model_path, metrics_path)
