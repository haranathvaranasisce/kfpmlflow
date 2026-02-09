"""Configuration constants for KFP components."""

# Container image configuration
BASE_IMAGE = 'python:3.11'
TARGET_IMAGE = 'gcr.io/my-project/my-component:v1'

# Pipeline configuration
PIPELINE_NAME = 'ml-training-pipeline'
PIPELINE_DESCRIPTION = 'A machine learning pipeline with data preparation, training, and scoring'
