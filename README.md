# KFP MLflow - KFP V2 Containerized ML Pipeline

This repository contains a Kubeflow Pipelines (KFP) V2 implementation of a machine learning pipeline with three main components:
- **dataprep**: Data preparation component that outputs train and test datasets
- **train**: Training component that takes train dataset and outputs metrics and model
- **score**: Scoring component that takes model and test data to generate predictions

All components utilize a shared `common` module with reusable utilities that are accessible at pipeline runtime.

## Project Structure

```
kfpmlflow/
├── common/              # Shared utilities module
│   ├── __init__.py
│   └── utils.py        # Contains check() function used by all components
├── dataprep/           # Data preparation module
│   ├── __init__.py
│   └── dataprep.py     # Dataprep component implementation
├── train/              # Training module
│   ├── __init__.py
│   └── train.py        # Training component implementation
├── score/              # Scoring/prediction module
│   ├── __init__.py
│   └── score.py        # Scoring component implementation
├── pipeline.py         # Main KFP V2 pipeline definition
├── pipeline_with_common.py  # Alternative pipeline with embedded common code
├── requirements.txt    # Python dependencies
├── setup.py           # Package setup for commons module
└── README.md          # This file
```

## Features

- **KFP V2 Components**: Uses latest Kubeflow Pipelines V2 SDK with Python function-based components
- **Containerized Execution**: Each component runs in its own container with specified base_image
- **Shared Commons Module**: All components can import and use the `common.utils` module
- **ML Workflow**: Complete ML pipeline from data prep through training to scoring
- **Type Annotations**: Proper use of Input/Output types for datasets, models, and metrics

## Common Module

The `common/utils.py` module contains shared utilities:

```python
def check(component_name: str) -> str:
    """
    Check function that can be called from any component.
    Validates component initialization and logs execution.
    """
```

This function is called by all three components (dataprep, train, score) to demonstrate shared code usage.

## Pipeline Components

### 1. Data Preparation (dataprep)
- **Inputs**: None
- **Outputs**: 
  - `train_data`: Training dataset (CSV)
  - `test_data`: Test dataset (CSV)
- **Function**: Creates sample datasets for training and testing

### 2. Training (train)
- **Inputs**: 
  - `train_data`: Training dataset from dataprep
- **Outputs**: 
  - `model`: Trained scikit-learn model (pickle)
  - `metrics`: Training metrics (JSON)
- **Function**: Trains a logistic regression model and computes metrics

### 3. Scoring (score)
- **Inputs**: 
  - `model`: Trained model from train component
  - `test_data`: Test dataset from dataprep
- **Outputs**: 
  - `predictions`: Predictions on test data (CSV)
  - `scores`: Test metrics (JSON)
- **Function**: Generates predictions and computes test metrics

## Usage

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install package to make common module accessible
pip install -e .
```

### Compile Pipeline

```bash
# Compile the main pipeline
python pipeline.py

# Or compile the alternative pipeline
python pipeline_with_common.py
```

This will generate a YAML file that can be uploaded to Kubeflow Pipelines.

### Run Pipeline

The compiled YAML can be uploaded and executed through the Kubeflow Pipelines UI or using the KFP SDK:

```python
from kfp import Client

client = Client(host='<your-kubeflow-host>')
client.create_run_from_pipeline_package(
    'ml_pipeline.yaml',
    arguments={},
    run_name='ml-pipeline-run'
)
```

## Base and Target Images

The pipeline uses:
- **BASE_IMAGE**: `python:3.9` - Base image for all components
- **TARGET_IMAGE**: `python:3.9` - Target image for component execution

Additional packages (pandas, scikit-learn) are installed at runtime via `packages_to_install` parameter.

## Dependencies

Key dependencies include:
- `kfp>=2.5.0` - Kubeflow Pipelines SDK
- `pandas>=2.0.3` - Data manipulation
- `scikit-learn>=1.3.0` - Machine learning
- `numpy>=1.24.3` - Numerical computing

## Development

### Adding New Components

1. Create a new module directory under the project root
2. Add component logic that imports from `common.utils`
3. Define the component in `pipeline.py` using `@component` decorator
4. Connect the component in the pipeline workflow

### Extending Common Module

Add new utility functions to `common/utils.py` that can be imported by any component:

```python
# In common/utils.py
def new_utility_function():
    # Implementation
    pass

# In any component
from common.utils import new_utility_function
```

## License

[Add your license information here]