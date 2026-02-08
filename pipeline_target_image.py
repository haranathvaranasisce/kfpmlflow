"""
KFP V2 Pipeline using custom target image with pre-installed common module.

This version demonstrates how to build and use a custom Docker image that already
contains the common module, eliminating the need to inline the code in each component.

Build the custom image first:
    docker build -t my-registry/kfpmlflow:latest .
    docker push my-registry/kfpmlflow:latest

Then use it as TARGET_IMAGE in this pipeline.
"""

from kfp import dsl
from kfp.dsl import component, pipeline, Output, Input, Dataset, Model, Metrics


# Use custom image that has common module pre-installed
BASE_IMAGE = "python:3.9"  # Base image for building
TARGET_IMAGE = "my-registry/kfpmlflow:latest"  # Custom image with common module


@component(
    base_image=TARGET_IMAGE,  # Use custom image with common module
    packages_to_install=[]  # Dependencies already in image
)
def dataprep_with_target_image(
    train_data: Output[Dataset],
    test_data: Output[Dataset]
):
    """
    Data preparation using pre-built target image with common module.
    """
    # Import from common module (available in target image)
    from common.utils import check
    import pandas as pd
    
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
    base_image=TARGET_IMAGE,
    packages_to_install=[]
)
def train_with_target_image(
    train_data: Input[Dataset],
    model: Output[Model],
    metrics: Output[Metrics]
):
    """
    Training using pre-built target image with common module.
    """
    from common.utils import check
    import pandas as pd
    import json
    import pickle
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    
    check("train")
    
    print(f"Loading training data...")
    train_df = pd.read_csv(train_data.path)
    
    # Prepare features and target
    X_train = train_df[['feature1', 'feature2']]
    y_train = train_df['target']
    
    # Train model
    print(f"Training model on {len(train_df)} samples...")
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
    
    # Save model and metrics
    with open(model.path, 'wb') as f:
        pickle.dump(trained_model, f)
    
    with open(metrics.path, 'w') as f:
        json.dump(metrics_dict, f, indent=2)
    
    metrics.log_metric('accuracy', metrics_dict['accuracy'])
    metrics.log_metric('precision', metrics_dict['precision'])
    metrics.log_metric('recall', metrics_dict['recall'])


@component(
    base_image=TARGET_IMAGE,
    packages_to_install=[]
)
def score_with_target_image(
    model: Input[Model],
    test_data: Input[Dataset],
    predictions: Output[Dataset],
    scores: Output[Metrics]
):
    """
    Scoring using pre-built target image with common module.
    """
    from common.utils import check
    import pandas as pd
    import json
    import pickle
    from sklearn.metrics import accuracy_score, precision_score, recall_score
    
    check("score")
    
    print("Loading model and test data...")
    
    # Load model
    with open(model.path, 'rb') as f:
        trained_model = pickle.load(f)
    
    # Load test data
    test_df = pd.read_csv(test_data.path)
    
    # Make predictions
    X_test = test_df[['feature1', 'feature2']]
    y_test = test_df['target']
    
    print(f"Scoring {len(test_df)} samples...")
    y_pred = trained_model.predict(X_test)
    
    # Calculate scores
    scores_dict = {
        'test_accuracy': float(accuracy_score(y_test, y_pred)),
        'test_precision': float(precision_score(y_test, y_pred, zero_division=0)),
        'test_recall': float(recall_score(y_test, y_pred, zero_division=0))
    }
    
    print(f"Test scores: {scores_dict}")
    
    # Save predictions and scores
    predictions_df = test_df.copy()
    predictions_df['predictions'] = y_pred
    predictions_df.to_csv(predictions.path, index=False)
    
    with open(scores.path, 'w') as f:
        json.dump(scores_dict, f, indent=2)
    
    scores.log_metric('test_accuracy', scores_dict['test_accuracy'])
    scores.log_metric('test_precision', scores_dict['test_precision'])
    scores.log_metric('test_recall', scores_dict['test_recall'])


@pipeline(
    name="ml-pipeline-with-target-image",
    description="ML pipeline using custom target image with pre-installed common module"
)
def ml_pipeline_with_target():
    """
    Pipeline using custom target image with common module pre-installed.
    """
    dataprep_task = dataprep_with_target_image()
    train_task = train_with_target_image(train_data=dataprep_task.outputs['train_data'])
    score_task = score_with_target_image(
        model=train_task.outputs['model'],
        test_data=dataprep_task.outputs['test_data']
    )


if __name__ == "__main__":
    from kfp import compiler
    
    print("Note: This pipeline requires a custom Docker image with common module.")
    print("Build the image first using: docker build -t my-registry/kfpmlflow:latest .")
    print("Then update TARGET_IMAGE in this file to point to your registry.")
    print()
    
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline_with_target,
        package_path='ml_pipeline_target_image.yaml'
    )
    print("Pipeline compiled successfully to ml_pipeline_target_image.yaml")
