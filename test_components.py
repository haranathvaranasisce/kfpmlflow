#!/usr/bin/env python3
"""
Simple test script to validate component functionality.
This script tests each component independently to ensure they work correctly.
"""
import sys
import tempfile
import os


def test_components():
    """Test all three components."""
    print("Testing KFP Components...")
    print("-" * 50)
    
    # Import components
    try:
        from src.dataprep import dataprep
        from src.train import train
        from src.score import score
        print("✓ Successfully imported all components")
    except ImportError as e:
        print(f"✗ Failed to import components: {e}")
        return False
    
    # Create temporary directory for test outputs
    with tempfile.TemporaryDirectory() as tmpdir:
        print("\n1. Testing dataprep component...")
        try:
            prepared_data_path = os.path.join(tmpdir, "prepared_data.json")
            result = dataprep.python_func(
                input_data_path="",
                output_data_path=prepared_data_path
            )
            print(f"   Result: {result}")
            print(f"   Output file exists: {os.path.exists(prepared_data_path)}")
            print("   ✓ dataprep component works!")
        except Exception as e:
            print(f"   ✗ dataprep failed: {e}")
            return False
        
        print("\n2. Testing train component...")
        try:
            model_path = os.path.join(tmpdir, "model.pkl")
            result = train.python_func(
                prepared_data_path=prepared_data_path,
                model_path=model_path
            )
            print(f"   Result: {result}")
            print(f"   Model file exists: {os.path.exists(model_path)}")
            print("   ✓ train component works!")
        except Exception as e:
            print(f"   ✗ train failed: {e}")
            return False
        
        print("\n3. Testing score component...")
        try:
            predictions_path = os.path.join(tmpdir, "predictions.json")
            result = score.python_func(
                model_path=model_path,
                prepared_data_path=prepared_data_path,
                predictions_path=predictions_path
            )
            print(f"   Result: {result}")
            print(f"   Predictions file exists: {os.path.exists(predictions_path)}")
            print("   ✓ score component works!")
        except Exception as e:
            print(f"   ✗ score failed: {e}")
            return False
    
    print("\n" + "=" * 50)
    print("✓ All component tests passed!")
    print("=" * 50)
    return True


def test_pipeline_compilation():
    """Test pipeline compilation."""
    print("\nTesting pipeline compilation...")
    print("-" * 50)
    
    try:
        from src.pipeline import ml_pipeline
        from kfp import compiler
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline_path = os.path.join(tmpdir, "test_pipeline.yaml")
            compiler.Compiler().compile(
                pipeline_func=ml_pipeline,
                package_path=pipeline_path
            )
            
            if os.path.exists(pipeline_path):
                print(f"✓ Pipeline compiled successfully to {pipeline_path}")
                # Check file size
                size = os.path.getsize(pipeline_path)
                print(f"  Pipeline YAML size: {size} bytes")
                return True
            else:
                print("✗ Pipeline compilation failed - no output file")
                return False
                
    except Exception as e:
        print(f"✗ Pipeline compilation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("KFP MLflow Component Test Suite")
    print("=" * 50)
    
    success = True
    
    # Test components
    if not test_components():
        success = False
    
    # Test pipeline compilation
    if not test_pipeline_compilation():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("✓ ALL TESTS PASSED!")
        print("=" * 50)
        sys.exit(0)
    else:
        print("✗ SOME TESTS FAILED")
        print("=" * 50)
        sys.exit(1)
