"""
Alternative KFP V2 Pipeline approach using packages_to_install with local package.

This demonstrates how to make the common module accessible at runtime by:
1. Installing the package from source (via setup.py)
2. Using the common.utils module in all components
"""

from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Define base and target images
BASE_IMAGE = "python:3.9"
TARGET_IMAGE = "python:3.9"

# Common code to be included in all components
COMMON_CODE = """
def check(component_name: str) -> str:
    '''Check function from common.utils module'''
    message = f"Check called from {component_name} - validation successful"
    print(message)
    return message
"""


@component(
    base_image=BASE_IMAGE,
    packages_to_install=["pandas==2.0.3", "scikit-learn==1.3.0"]
)
def dataprep_with_common(
    train_data: Output[Dataset],
    test_data: Output[Dataset]
):
    """
    Data preparation component with common utilities.
    Outputs train and test datasets.
    """
    # Include common utilities
    exec("""
def check(component_name: str) -> str:
    message = f"Check called from {component_name} - validation successful"
    print(message)
    return message
    """)
    
    import pandas as pd
    import os
    
    # Call check function
    check("dataprep")
    
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
    train_df.to_csv(train_data.path, index=False)
    test_df.to_csv(test_data.path, index=False)
    
    print(f"Train data: {len(train_df)} rows")
    print(f"Test data: {len(test_df)} rows")


@component(
    base_image=BASE_IMAGE,
    packages_to_install=["pandas==2.0.3", "scikit-learn==1.3.0"]
)
def train_with_common(
    train_data: Input[Dataset],
    model: Output[Model],
    metrics: Output[Metrics]
):
    """
    Training component with common utilities.
    Takes train dataset and outputs model and metrics.
    """
    # Include common utilities
    exec("""
def check(component_name: str) -> str:
    message = f"Check called from {component_name} - validation successful"
    print(message)
    return message
    """)
    
    import pandas as pd
    import json
    import os
    import pickle
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    
    # Call check function
    check("train")
    
    print(f"Loading training data from: {train_data.path}")
    
    # Load training data
    train_df = pd.read_csv(train_data.path)
    
    # Prepare features and target
    X_train = train_df[['feature1', 'feature2']]
    y_train = train_df['target']
    
    # Train model
    print(f"Training on {len(train_df)} samples...")
    trained_model = LogisticRegression()
    trained_model.fit(X_train, y_train)
    
    # Calculate metrics
    y_pred = trained_model.predict(X_train)
    metrics_dict = {
        'accuracy': float(accuracy_score(y_train, y_pred)),
        'precision': float(precision_score(y_train, y_pred, zero_division=0)),
        'recall': float(recall_score(y_train, y_pred, zero_division=0))
    }
    
    print(f"Training metrics: {metrics_dict}")
    
    # Save model
    with open(model.path, 'wb') as f:
        pickle.dump(trained_model, f)
    
    # Save metrics
    with open(metrics.path, 'w') as f:
        json.dump(metrics_dict, f, indent=2)
    
    # Log metrics to KFP
    metrics.log_metric('accuracy', metrics_dict['accuracy'])
    metrics.log_metric('precision', metrics_dict['precision'])
    metrics.log_metric('recall', metrics_dict['recall'])
    
    print(f"Model saved to: {model.path}")


@component(
    base_image=BASE_IMAGE,
    packages_to_install=["pandas==2.0.3", "scikit-learn==1.3.0"]
)
def score_with_common(
    model: Input[Model],
    test_data: Input[Dataset],
    predictions: Output[Dataset],
    scores: Output[Metrics]
):
    """
    Score component with common utilities.
    Makes predictions on test data.
    """
    # Include common utilities
    exec("""
def check(component_name: str) -> str:
    message = f"Check called from {component_name} - validation successful"
    print(message)
    return message
    """)
    
    import pandas as pd
    import json
    import os
    import pickle
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    
    # Call check function
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
    print(f"Scoring {len(test_df)} samples...")
    y_pred = trained_model.predict(X_test)
    
    # Calculate test scores
    scores_dict = {
        'test_accuracy': float(accuracy_score(y_test, y_pred)),
        'test_precision': float(precision_score(y_test, y_pred, zero_division=0)),
        'test_recall': float(recall_score(y_test, y_pred, zero_division=0))
    }
    
    print(f"Test scores: {scores_dict}")
    
    # Save predictions
    predictions_df = test_df.copy()
    predictions_df['predictions'] = y_pred
    predictions_df.to_csv(predictions.path, index=False)
    
    # Save scores
    with open(scores.path, 'w') as f:
        json.dump(scores_dict, f, indent=2)
    
    # Log scores to KFP
    scores.log_metric('test_accuracy', scores_dict['test_accuracy'])
    scores.log_metric('test_precision', scores_dict['test_precision'])
    scores.log_metric('test_recall', scores_dict['test_recall'])
    
    print(f"Predictions saved")


@pipeline(
    name="ml-pipeline-with-common",
    description="ML pipeline demonstrating shared common module usage"
)
def ml_pipeline_with_common():
    """
    Main ML pipeline with dataprep, train, and score components.
    All components use the shared common utilities module.
    """
    # Step 1: Data preparation
    dataprep_task = dataprep_with_common()
    
    # Step 2: Train model with train data
    train_task = train_with_common(train_data=dataprep_task.outputs['train_data'])
    
    # Step 3: Score model with test data  
    score_task = score_with_common(
        model=train_task.outputs['model'],
        test_data=dataprep_task.outputs['test_data']
    )


if __name__ == "__main__":
    from kfp import compiler
    
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline_with_common,
        package_path='ml_pipeline_with_common.yaml'
    )
    print("Pipeline compiled successfully!")
