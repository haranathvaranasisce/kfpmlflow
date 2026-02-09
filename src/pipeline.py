"""ML Pipeline that orchestrates dataprep, train, and score components."""
from kfp import dsl
from kfp import compiler

# Import the component functions
from dataprep import dataprep
from train import train
from score import score


@dsl.pipeline(
    name='ml-training-pipeline',
    description='A machine learning pipeline with data preparation, training, and scoring'
)
def ml_pipeline(
    input_data_path: str = 'gs://my-bucket/input-data'
):
    """
    Machine Learning Pipeline
    
    This pipeline orchestrates three containerized components:
    1. dataprep: Prepares and preprocesses data
    2. train: Trains a machine learning model
    3. score: Scores/evaluates the trained model
    
    Args:
        input_data_path: Path to the input data
    """
    # Step 1: Data preparation
    dataprep_task = dataprep(input_data_path=input_data_path)
    
    # Step 2: Model training (depends on dataprep)
    train_task = train(prepared_data_path=dataprep_task.outputs['output_data_path'])
    
    # Step 3: Model scoring (depends on train and dataprep)
    score_task = score(
        model_path=train_task.outputs['model_path'],
        prepared_data_path=dataprep_task.outputs['output_data_path']
    )


if __name__ == '__main__':
    """Compile the pipeline to a YAML file."""
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline,
        package_path='ml_pipeline.yaml'
    )
    print("Pipeline compiled successfully to ml_pipeline.yaml")
