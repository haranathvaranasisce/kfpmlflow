"""
KFP V2 Pipeline for ML workflow with dataprep, train, and score components.

This pipeline demonstrates containerized Python components with shared commons module.
"""

from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define base image with common dependencies
BASE_IMAGE = "python:3.9"
TARGET_IMAGE = "python:3.9"


@component(
    base_image=BASE_IMAGE,
    packages_to_install=[
        "pandas==2.0.3",
        "scikit-learn==1.3.0",
    ]
)
def dataprep_op() -> tuple[Dataset, Dataset]:
    """
    Data preparation component that outputs train and test datasets.
    
    Returns:
        Tuple of (train_dataset, test_dataset)
    """
    # Define the check function inline to ensure it's available at runtime
    def check(component_name: str) -> str:
        """Check function from common.utils"""
        message = f"Check called from {component_name} - validation successful"
        print(message)
        return message
    
    check("dataprep")
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
    
    return train_path, test_path


@component(
    base_image=BASE_IMAGE,
    packages_to_install=[
        "pandas==2.0.3",
        "scikit-learn==1.3.0",
    ]
)
def train_op(train_data: Input[Dataset]) -> tuple[Model, Metrics]:
    """
    Training component that takes train dataset and outputs metrics and model.
    
    Args:
        train_data: Training dataset path
        
    Returns:
        Tuple of (model, metrics)
    """
    # Define the check function inline to ensure it's available at runtime
    def check(component_name: str) -> str:
        """Check function from common.utils"""
        message = f"Check called from {component_name} - validation successful"
        print(message)
        return message
    
    check("train")
    import pandas as pd
    import json
    import os
    import pickle
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    
    # Call check function from commons
    check("train")
    
    print(f"Loading training data from: {train_data.path}")
    
    # Load training data
    train_df = pd.read_csv(train_data.path)
    
    # Prepare features and target
    X_train = train_df[['feature1', 'feature2']]
    y_train = train_df['target']
    
    # Train model
    print("Training logistic regression model...")
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # Calculate metrics
    y_pred = model.predict(X_train)
    metrics_dict = {
        'accuracy': float(accuracy_score(y_train, y_pred)),
        'precision': float(precision_score(y_train, y_pred, zero_division=0)),
        'recall': float(recall_score(y_train, y_pred, zero_division=0))
    }
    
    print(f"Training metrics: {metrics_dict}")
    
    # Save model and metrics
    os.makedirs('/tmp/models', exist_ok=True)
    model_path = '/tmp/models/model.pkl'
    metrics_path = '/tmp/models/metrics.json'
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    with open(metrics_path, 'w') as f:
        json.dump(metrics_dict, f, indent=2)
    
    print(f"Model saved to: {model_path}")
    print(f"Metrics saved to: {metrics_path}")
    
    return model_path, metrics_path


@component(
    base_image=BASE_IMAGE,
    packages_to_install=[
        "pandas==2.0.3",
        "scikit-learn==1.3.0",
    ]
)
def score_op(model: Input[Model], test_data: Input[Dataset]) -> tuple[Dataset, Metrics]:
    """
    Score component that loads model and makes predictions on test data.
    
    Args:
        model: Trained model path
        test_data: Test dataset path
        
    Returns:
        Tuple of (predictions, scores)
    """
    # Define the check function inline to ensure it's available at runtime
    def check(component_name: str) -> str:
        """Check function from common.utils"""
        message = f"Check called from {component_name} - validation successful"
        print(message)
        return message
    
    check("score")
    import pandas as pd
    import json
    import os
    import pickle
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    
    # Call check function from commons
    check("score")
    
    print(f"Loading model from: {model.path}")
    print(f"Loading test data from: {test_data.path}")
    
    # Load model
    with open(model.path, 'rb') as f:
        trained_model = pickle.load(f)
    
    # Load test data
    test_df = pd.read_csv(test_data.path)
    
    # Prepare features and target
    X_test = test_df[['feature1', 'feature2']]
    y_test = test_df['target']
    
    # Make predictions
    print("Making predictions on test data...")
    y_pred = trained_model.predict(X_test)
    
    # Calculate test scores
    scores_dict = {
        'test_accuracy': float(accuracy_score(y_test, y_pred)),
        'test_precision': float(precision_score(y_test, y_pred, zero_division=0)),
        'test_recall': float(recall_score(y_test, y_pred, zero_division=0))
    }
    
    print(f"Test scores: {scores_dict}")
    
    # Save predictions and scores
    os.makedirs('/tmp/predictions', exist_ok=True)
    predictions_path = '/tmp/predictions/predictions.csv'
    scores_path = '/tmp/predictions/scores.json'
    
    predictions_df = test_df.copy()
    predictions_df['predictions'] = y_pred
    predictions_df.to_csv(predictions_path, index=False)
    
    with open(scores_path, 'w') as f:
        json.dump(scores_dict, f, indent=2)
    
    print(f"Predictions saved to: {predictions_path}")
    print(f"Scores saved to: {scores_path}")
    
    return predictions_path, scores_path


@pipeline(
    name="ml-pipeline",
    description="A ML pipeline with dataprep, train, and score components"
)
def ml_pipeline():
    """
    Main ML pipeline orchestrating dataprep, train, and score components.
    """
    # Step 1: Data preparation
    dataprep_task = dataprep_op()
    
    # Step 2: Train model with train data
    train_task = train_op(train_data=dataprep_task.outputs['output_0'])
    
    # Step 3: Score model with test data
    score_task = score_op(
        model=train_task.outputs['output_0'],
        test_data=dataprep_task.outputs['output_1']
    )


if __name__ == "__main__":
    # For local testing or compilation
    from kfp import compiler
    
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline,
        package_path='ml_pipeline.yaml'
    )
    print("Pipeline compiled successfully to ml_pipeline.yaml")
