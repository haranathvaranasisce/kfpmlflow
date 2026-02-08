"""Score/prediction component for KFP V2 pipeline."""

from typing import NamedTuple


def score_component(model: str, test_data: str) -> NamedTuple('ScoreOutputs', [('predictions', str), ('scores', str)]):
    """
    Score component that loads model and makes predictions on test data.
    
    Args:
        model: Path to trained model
        test_data: Path to test dataset
        
    Returns:
        NamedTuple containing paths to predictions and scores
    """
    from common.utils import check
    from collections import namedtuple
    import pandas as pd
    import json
    import os
    import pickle
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    
    # Call check function from commons
    check("score")
    
    print(f"Loading model from: {model}")
    print(f"Loading test data from: {test_data}")
    
    # Load model
    with open(model, 'rb') as f:
        trained_model = pickle.load(f)
    
    # Load test data
    test_df = pd.read_csv(test_data)
    
    # Prepare features and target
    X_test = test_df[['feature1', 'feature2']]
    y_test = test_df['target']
    
    # Make predictions
    print("Making predictions on test data...")
    y_pred = trained_model.predict(X_test)
    
    # Calculate test scores
    scores = {
        'test_accuracy': float(accuracy_score(y_test, y_pred)),
        'test_precision': float(precision_score(y_test, y_pred, zero_division=0)),
        'test_recall': float(recall_score(y_test, y_pred, zero_division=0))
    }
    
    print(f"Test scores: {scores}")
    
    # Save predictions and scores
    os.makedirs('/tmp/predictions', exist_ok=True)
    predictions_path = '/tmp/predictions/predictions.csv'
    scores_path = '/tmp/predictions/scores.json'
    
    predictions_df = test_df.copy()
    predictions_df['predictions'] = y_pred
    predictions_df.to_csv(predictions_path, index=False)
    
    with open(scores_path, 'w') as f:
        json.dump(scores, f, indent=2)
    
    print(f"Predictions saved to: {predictions_path}")
    print(f"Scores saved to: {scores_path}")
    
    # Return outputs
    ScoreOutputs = namedtuple('ScoreOutputs', ['predictions', 'scores'])
    return ScoreOutputs(predictions_path, scores_path)
