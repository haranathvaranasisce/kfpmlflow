"""
Test script to validate individual components before pipeline compilation.
This tests that each component can run independently and the common module is accessible.
"""

import sys
import os

# Add the project root to Python path to make common module accessible
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_common_utils():
    """Test that common.utils module can be imported and check() function works."""
    print("\n=== Testing common.utils module ===")
    from common.utils import check
    
    result = check("test")
    assert "test" in result
    assert "validation successful" in result
    print("✓ common.utils.check() works correctly")


def test_dataprep_component():
    """Test the dataprep component."""
    print("\n=== Testing dataprep component ===")
    from dataprep.dataprep import dataprep_component
    
    result = dataprep_component()
    train_path, test_path = result.train_data, result.test_data
    
    assert os.path.exists(train_path), f"Train data not found at {train_path}"
    assert os.path.exists(test_path), f"Test data not found at {test_path}"
    print(f"✓ Dataprep component created train data at: {train_path}")
    print(f"✓ Dataprep component created test data at: {test_path}")
    
    return train_path, test_path


def test_train_component(train_path):
    """Test the train component."""
    print("\n=== Testing train component ===")
    from train.train import train_component
    
    result = train_component(train_path)
    model_path, metrics_path = result.model, result.metrics
    
    assert os.path.exists(model_path), f"Model not found at {model_path}"
    assert os.path.exists(metrics_path), f"Metrics not found at {metrics_path}"
    print(f"✓ Train component created model at: {model_path}")
    print(f"✓ Train component created metrics at: {metrics_path}")
    
    # Read and display metrics
    import json
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    print(f"  Training metrics: {metrics}")
    
    return model_path, metrics_path


def test_score_component(model_path, test_path):
    """Test the score component."""
    print("\n=== Testing score component ===")
    from score.score import score_component
    
    result = score_component(model_path, test_path)
    predictions_path, scores_path = result.predictions, result.scores
    
    assert os.path.exists(predictions_path), f"Predictions not found at {predictions_path}"
    assert os.path.exists(scores_path), f"Scores not found at {scores_path}"
    print(f"✓ Score component created predictions at: {predictions_path}")
    print(f"✓ Score component created scores at: {scores_path}")
    
    # Read and display scores
    import json
    with open(scores_path, 'r') as f:
        scores = json.load(f)
    print(f"  Test scores: {scores}")


def main():
    """Run all component tests."""
    print("=" * 60)
    print("Testing KFP ML Pipeline Components")
    print("=" * 60)
    
    try:
        # Test common module
        test_common_utils()
        
        # Test dataprep component
        train_path, test_path = test_dataprep_component()
        
        # Test train component
        model_path, metrics_path = test_train_component(train_path)
        
        # Test score component
        test_score_component(model_path, test_path)
        
        print("\n" + "=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
