# kfpmlflow

A Kubeflow Pipelines (KFP) project with containerized Python components for machine learning workflows.

## Overview

This project implements a complete ML pipeline using Kubeflow Pipelines with three containerized components:

1. **dataprep**: Data preparation and preprocessing component
2. **train**: Model training component
3. **score**: Model evaluation and scoring component

All components are containerized Python components using the `@dsl.component` decorator with:
- Base image: `python:3.11`
- Target image: `gcr.io/my-project/my-component:v1`

## Project Structure

```
kfpmlflow/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── dataprep.py       # Data preparation component
│   ├── train.py          # Model training component
│   ├── score.py          # Model scoring component
│   └── pipeline.py       # Pipeline orchestration
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .gitignore           # Git ignore patterns
```

## Components

### 1. Data Preparation Component (`dataprep`)

**Purpose**: Prepares and preprocesses data for training.

**Decorator**:
```python
@dsl.component(
    base_image='python:3.11',
    target_image='gcr.io/my-project/my-component:v1'
)
```

**Inputs**:
- `input_data_path` (str): Path to the input data

**Outputs**:
- `output_data_path` (str): Path to the processed data
- Returns status message

**Functionality**:
- Loads raw data
- Performs data normalization
- Saves processed data in JSON format

### 2. Model Training Component (`train`)

**Purpose**: Trains a machine learning model on prepared data.

**Decorator**:
```python
@dsl.component(
    base_image='python:3.11',
    target_image='gcr.io/my-project/my-component:v1'
)
```

**Inputs**:
- `prepared_data_path` (str): Path to the prepared data

**Outputs**:
- `model_path` (str): Path to the trained model
- Returns training metrics (accuracy scores)

**Functionality**:
- Loads prepared data
- Trains a Logistic Regression model
- Evaluates on train and test sets
- Saves model using pickle

### 3. Model Scoring Component (`score`)

**Purpose**: Evaluates the trained model and generates predictions.

**Decorator**:
```python
@dsl.component(
    base_image='python:3.11',
    target_image='gcr.io/my-project/my-component:v1'
)
```

**Inputs**:
- `model_path` (str): Path to the trained model
- `prepared_data_path` (str): Path to the data for scoring

**Outputs**:
- `predictions_path` (str): Path to the predictions
- Returns scoring metrics

**Functionality**:
- Loads trained model
- Makes predictions on data
- Calculates accuracy metrics
- Saves predictions and probabilities

## Pipeline Architecture

The `ml_pipeline` orchestrates all three components in sequence:

```
Input Data → [dataprep] → Prepared Data → [train] → Model → [score] → Predictions
                                            ↓
                                    Prepared Data
```

## Installation

```bash
# Clone the repository
git clone https://github.com/haranathvaranasisce/kfpmlflow.git
cd kfpmlflow

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Compile the Pipeline

```bash
cd src
python pipeline.py
```

This will generate a `ml_pipeline.yaml` file that can be uploaded to Kubeflow Pipelines.

### Using the Components

```python
from src import dataprep, train, score, ml_pipeline
from kfp import dsl

# Use in a pipeline
@dsl.pipeline(name='my-pipeline')
def my_custom_pipeline():
    dataprep_task = dataprep(input_data_path='gs://my-bucket/data')
    train_task = train(prepared_data_path=dataprep_task.outputs['output_data_path'])
    score_task = score(
        model_path=train_task.outputs['model_path'],
        prepared_data_path=dataprep_task.outputs['output_data_path']
    )
```

## Configuration

### Updating Docker Image

To use a different Docker image, update the `target_image` parameter in each component:

```python
@dsl.component(
    base_image='python:3.11',
    target_image='gcr.io/your-project/your-component:v1'  # Update this
)
```

### Customizing Components

Each component is self-contained and can be customized independently:

1. Modify the function logic in `dataprep.py`, `train.py`, or `score.py`
2. Keep the `@dsl.component` decorator unchanged
3. Recompile the pipeline using `python pipeline.py`

## Dependencies

Core dependencies:
- `kfp>=2.0.0` - Kubeflow Pipelines SDK
- `google-cloud-aiplatform` - Google Cloud AI Platform
- `pandas` - Data manipulation
- `scikit-learn` - Machine learning algorithms
- `mlflow` - ML experiment tracking

## Development

### Adding New Components

1. Create a new Python file in the `src/` directory
2. Define your component function with the `@dsl.component` decorator:
   ```python
   @dsl.component(
       base_image='python:3.11',
       target_image='gcr.io/my-project/my-component:v1'
   )
   def my_component(input_param: str) -> str:
       # Your logic here
       return "result"
   ```
3. Import and use the component in `pipeline.py`

### Testing Components

Components can be tested locally before deploying to KFP:

```python
from src.dataprep import dataprep

# Test the component function
result = dataprep(input_data_path='test-data', output_data_path='/tmp/output')
print(result)
```

## Deployment

### Prerequisites

1. Access to a Kubeflow Pipelines cluster
2. Docker registry (e.g., GCR) for storing container images
3. Proper authentication configured

### Steps

1. **Compile the pipeline**:
   ```bash
   cd src
   python pipeline.py
   ```

2. **Upload to Kubeflow**:
   - Navigate to the Kubeflow Pipelines UI
   - Click "Upload pipeline"
   - Select the generated `ml_pipeline.yaml` file

3. **Create a run**:
   - Select the uploaded pipeline
   - Click "Create run"
   - Provide input parameters
   - Start the run

## Container Images

All components use the same containerization approach:
- **Base image**: `python:3.11` provides the Python runtime
- **Target image**: `gcr.io/my-project/my-component:v1` is where the built container is pushed
- KFP automatically builds and pushes containers when you compile the pipeline

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on GitHub.