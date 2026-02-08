# KFP V2 Pipeline - Usage Guide

This guide explains how to use the KFP V2 ML pipeline with different approaches for making the common module accessible at runtime.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Pipeline Variants](#pipeline-variants)
3. [Common Module Usage](#common-module-usage)
4. [Building Custom Images](#building-custom-images)
5. [Running the Pipeline](#running-the-pipeline)

## Quick Start

### Prerequisites

- Python 3.9+
- Docker (for building custom images)
- Kubeflow Pipelines cluster (for running pipelines)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd kfpmlflow

# Install dependencies
pip install -r requirements.txt

# Install the package (makes common module available)
pip install -e .
```

## Pipeline Variants

This project provides three pipeline variants:

### 1. pipeline_v2.py (Recommended)

**Approach**: Inlines the common utilities directly in each component.

**Pros**:
- No custom image build required
- Works with any base image
- Simple deployment

**Cons**:
- Code duplication across components
- Changes to common utilities require updating all components

**Usage**:
```bash
python pipeline_v2.py
# Generates: ml_pipeline.yaml
```

### 2. pipeline_target_image.py

**Approach**: Uses a custom-built Docker image with common module pre-installed.

**Pros**:
- Clean component code - imports from common module
- Single source of truth for common utilities
- Faster component startup (no runtime installations)

**Cons**:
- Requires building and maintaining custom Docker image
- Image must be pushed to a registry accessible by Kubeflow

**Usage**:
```bash
# 1. Build custom image
./build_image.sh

# 2. Update TARGET_IMAGE in pipeline_target_image.py
# 3. Compile pipeline
python pipeline_target_image.py
# Generates: ml_pipeline_target_image.yaml
```

### 3. pipeline_with_common.py (Alternative)

**Approach**: Uses `exec()` to inject common code at runtime.

**Usage**:
```bash
python pipeline_with_common.py
# Generates: ml_pipeline_with_common.yaml
```

## Common Module Usage

All three pipelines use the `common.utils.check()` function in each component:

```python
from common.utils import check  # In target image approach

# Or inline:
def check(component_name: str) -> str:
    message = f"Check called from {component_name} - validation successful"
    print(message)
    return message

# Usage in components
check("dataprep")  # Called in dataprep component
check("train")     # Called in train component  
check("score")     # Called in score component
```

### Adding New Utilities

To add new utilities to the common module:

1. Edit `common/utils.py`:
```python
def my_new_function(param):
    """New utility function"""
    # Implementation
    pass
```

2. Use in components:
```python
from common.utils import check, my_new_function

check("my-component")
my_new_function(value)
```

## Building Custom Images

### Using the Build Script

```bash
# Edit build_image.sh to configure your registry
./build_image.sh
```

### Manual Build

```bash
# Build image
docker build -t my-registry/kfpmlflow:v1.0.0 .

# Push to registry
docker push my-registry/kfpmlflow:v1.0.0

# Update pipeline_target_image.py
# TARGET_IMAGE = "my-registry/kfpmlflow:v1.0.0"
```

### Dockerfile Structure

The Dockerfile:
1. Uses Python 3.9 base image
2. Installs dependencies from requirements.txt
3. Copies the common module
4. Installs the package with `pip install -e .`
5. Sets PYTHONPATH for module accessibility

## Running the Pipeline

### 1. Compile Pipeline

```bash
# Choose your variant
python pipeline_v2.py
```

This generates a YAML file (e.g., `ml_pipeline.yaml`).

### 2. Upload to Kubeflow

**Option A: Via UI**
1. Open Kubeflow Pipelines UI
2. Go to "Pipelines" → "Upload Pipeline"
3. Upload the generated YAML file
4. Create a run

**Option B: Via SDK**
```python
from kfp import Client

client = Client(host='https://your-kubeflow-host')

# Upload pipeline
pipeline_id = client.upload_pipeline(
    pipeline_package_path='ml_pipeline.yaml',
    pipeline_name='ML Pipeline V2'
)

# Create run
run = client.run_pipeline(
    experiment_id='<experiment-id>',
    job_name='ml-pipeline-run',
    pipeline_id=pipeline_id
)
```

### 3. Monitor Execution

In the Kubeflow UI:
1. Navigate to "Runs"
2. Select your run
3. View component logs
4. Check outputs and metrics

## Pipeline Components

### Dataprep Component
- **Outputs**: train_data (Dataset), test_data (Dataset)
- **Function**: Creates sample train and test datasets
- **Check**: Calls `check("dataprep")`

### Train Component
- **Inputs**: train_data (Dataset)
- **Outputs**: model (Model), metrics (Metrics)
- **Function**: Trains logistic regression model
- **Check**: Calls `check("train")`

### Score Component
- **Inputs**: model (Model), test_data (Dataset)
- **Outputs**: predictions (Dataset), scores (Metrics)
- **Function**: Generates predictions on test data
- **Check**: Calls `check("score")`

## Component Logs

Check the component logs to verify the common module is working:

```
Check called from dataprep - validation successful
Preparing training and test datasets...
Train data: 5 rows
Test data: 3 rows
```

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'common'**
- Using target image approach: Ensure image was built correctly and pushed to registry
- Using inline approach: Should not occur as code is inlined

**2. Image pull errors**
- Verify TARGET_IMAGE is correct
- Ensure Kubeflow cluster can access your registry
- Check image exists: `docker pull <image-name>`

**3. Component execution failures**
- Check component logs in Kubeflow UI
- Verify all required packages are installed
- Ensure base_image or target_image is accessible

## Best Practices

1. **Version your images**: Use semantic versioning (e.g., v1.0.0)
2. **Test locally**: Run test_components.py before deploying
3. **Use target images for production**: Faster, more reliable
4. **Keep common utilities small**: Only shared, reusable code
5. **Document changes**: Update README when modifying components

## Advanced Usage

### Custom Base Images

Create domain-specific base images with additional tools:

```dockerfile
FROM python:3.9
RUN apt-get update && apt-get install -y <your-tools>
COPY requirements.txt .
RUN pip install -r requirements.txt
```

### Environment Variables

Pass configuration via environment variables:

```python
@component(
    base_image=BASE_IMAGE,
    packages_to_install=['pandas==2.0.3']
)
def my_component():
    import os
    config_value = os.getenv('MY_CONFIG', 'default')
```

### Pipeline Parameters

Add runtime parameters to the pipeline:

```python
@pipeline(name="ml-pipeline-v2")
def ml_pipeline(
    learning_rate: float = 0.01,
    max_iterations: int = 100
):
    dataprep_task = dataprep_op()
    train_task = train_op(
        train_data=dataprep_task.outputs['train_data'],
        learning_rate=learning_rate,
        max_iterations=max_iterations
    )
```

## Support

For issues or questions:
1. Check the logs in Kubeflow UI
2. Review this usage guide
3. Check component implementation in source files
4. Consult KFP V2 documentation: https://www.kubeflow.org/docs/components/pipelines/

## License

[Add your license information here]
