#!/usr/bin/env python3
"""
Demonstration script to show that the common module is accessible
across all three components (dataprep, train, score).
"""
import tempfile
import os


def test_common_module_usage():
    """Test that all components can access and use the common module."""
    print("=" * 60)
    print("Testing Common Module Across All Components")
    print("=" * 60)
    
    # Import components
    from src.dataprep import dataprep
    from src.train import train
    from src.score import score
    
    print("\nRunning components to demonstrate common module usage:")
    print("-" * 60)
    
    # Create temporary directory for test outputs
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test dataprep
        print("\n1. Running dataprep component:")
        print("   Expected: 'Called from module: src.dataprep'")
        prepared_data_path = os.path.join(tmpdir, "prepared_data.json")
        result = dataprep.python_func(
            input_data_path="",
            output_data_path=prepared_data_path
        )
        print(f"   Status: {result}\n")
        
        # Test train
        print("2. Running train component:")
        print("   Expected: 'Called from module: src.train'")
        model_path = os.path.join(tmpdir, "model.pkl")
        result = train.python_func(
            prepared_data_path=prepared_data_path,
            model_path=model_path
        )
        print(f"   Status: {result}\n")
        
        # Test score
        print("3. Running score component:")
        print("   Expected: 'Called from module: src.score'")
        predictions_path = os.path.join(tmpdir, "predictions.json")
        result = score.python_func(
            model_path=model_path,
            prepared_data_path=prepared_data_path,
            predictions_path=predictions_path
        )
        print(f"   Status: {result}\n")
    
    print("=" * 60)
    print("✓ Common module successfully used across all components!")
    print("=" * 60)


if __name__ == "__main__":
    test_common_module_usage()
