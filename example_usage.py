#!/usr/bin/env python3
"""
Example script demonstrating how to use the KFP components and pipeline.

This script shows:
1. How to import and use individual components
2. How to compile the pipeline
3. How to create a custom pipeline using the components
"""

from src import dataprep, train, score, ml_pipeline
from kfp import dsl
from kfp import compiler


def example_using_default_pipeline():
    """Example: Compile the default ML pipeline."""
    print("=" * 60)
    print("Example 1: Using the default ML pipeline")
    print("=" * 60)
    
    # Compile the default pipeline
    compiler.Compiler().compile(
        pipeline_func=ml_pipeline,
        package_path='example_pipeline.yaml'
    )
    
    print("✓ Default pipeline compiled to 'example_pipeline.yaml'")
    print("\nTo run this pipeline on Kubeflow:")
    print("1. Upload 'example_pipeline.yaml' to Kubeflow Pipelines UI")
    print("2. Create a new run")
    print("3. Provide the input_data_path parameter")
    print()


def example_custom_pipeline():
    """Example: Create a custom pipeline using the components."""
    print("=" * 60)
    print("Example 2: Creating a custom pipeline")
    print("=" * 60)
    
    @dsl.pipeline(
        name='custom-ml-pipeline',
        description='A custom ML pipeline with modified parameters'
    )
    def custom_pipeline(
        input_data_path: str = 'gs://my-custom-bucket/data',
        enable_scoring: bool = True
    ):
        """Custom pipeline with conditional scoring."""
        
        # Step 1: Data preparation
        prep_task = dataprep(input_data_path=input_data_path)
        
        # Step 2: Training
        train_task = train(
            prepared_data_path=prep_task.outputs['output_data_path']
        )
        
        # Step 3: Conditional scoring
        if enable_scoring:
            score_task = score(
                model_path=train_task.outputs['model_path'],
                prepared_data_path=prep_task.outputs['output_data_path']
            )
    
    # Compile the custom pipeline
    compiler.Compiler().compile(
        pipeline_func=custom_pipeline,
        package_path='custom_pipeline.yaml'
    )
    
    print("✓ Custom pipeline compiled to 'custom_pipeline.yaml'")
    print()


def show_component_details():
    """Show details about each component."""
    print("=" * 60)
    print("Component Details")
    print("=" * 60)
    
    print("\n1. Data Preparation Component (dataprep)")
    print("   - Base Image: python:3.11")
    print("   - Target Image: gcr.io/my-project/my-component:v1")
    print("   - Input: input_data_path (str)")
    print("   - Output: output_data_path (str)")
    print("   - Function: Loads and preprocesses data")
    
    print("\n2. Training Component (train)")
    print("   - Base Image: python:3.11")
    print("   - Target Image: gcr.io/my-project/my-component:v1")
    print("   - Input: prepared_data_path (str)")
    print("   - Output: model_path (str)")
    print("   - Function: Trains a Logistic Regression model")
    
    print("\n3. Scoring Component (score)")
    print("   - Base Image: python:3.11")
    print("   - Target Image: gcr.io/my-project/my-component:v1")
    print("   - Inputs: model_path (str), prepared_data_path (str)")
    print("   - Output: predictions_path (str)")
    print("   - Function: Evaluates model and generates predictions")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("KFP MLflow - Component Usage Examples")
    print("=" * 60 + "\n")
    
    # Show component details
    show_component_details()
    
    # Example 1: Default pipeline
    example_using_default_pipeline()
    
    # Example 2: Custom pipeline
    example_custom_pipeline()
    
    print("=" * 60)
    print("Examples completed successfully!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - example_pipeline.yaml")
    print("  - custom_pipeline.yaml")
    print("\nNext steps:")
    print("  1. Review the generated YAML files")
    print("  2. Update target_image in components if needed")
    print("  3. Upload to Kubeflow Pipelines")
    print("  4. Create and run a pipeline execution")
    print()


if __name__ == "__main__":
    main()
