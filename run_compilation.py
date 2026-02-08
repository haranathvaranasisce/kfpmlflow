#!/usr/bin/env python3
"""
Simple runner script to compile all pipeline variants and show their outputs.
This script compiles all three pipeline variants and reports their status.
"""

import os
import sys
from pathlib import Path


def compile_pipeline(pipeline_file, expected_output):
    """Compile a pipeline and check if output was created."""
    print(f"\n{'='*60}")
    print(f"Compiling: {pipeline_file}")
    print('='*60)
    
    try:
        # Import and run the pipeline
        import subprocess
        result = subprocess.run(
            [sys.executable, pipeline_file],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✓ Compilation successful!")
            print(f"  Output: {result.stdout.strip()}")
            
            # Check if output file exists
            if os.path.exists(expected_output):
                file_size = os.path.getsize(expected_output)
                print(f"  Generated file: {expected_output} ({file_size} bytes)")
                return True
            else:
                print(f"  Warning: Expected output file not found: {expected_output}")
                return False
        else:
            print(f"✗ Compilation failed!")
            print(f"  Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Exception during compilation: {e}")
        return False


def main():
    """Main runner function."""
    print("="*60)
    print("KFP V2 Pipeline Compilation Runner")
    print("="*60)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    pipelines = [
        ("pipeline_v2.py", "ml_pipeline.yaml"),
        ("pipeline_with_common.py", "ml_pipeline_with_common.yaml"),
        # Skip target image pipeline as it requires custom image
        # ("pipeline_target_image.py", "ml_pipeline_target_image.yaml"),
    ]
    
    results = {}
    
    for pipeline_file, output_file in pipelines:
        if os.path.exists(pipeline_file):
            success = compile_pipeline(pipeline_file, output_file)
            results[pipeline_file] = success
        else:
            print(f"\n✗ Pipeline file not found: {pipeline_file}")
            results[pipeline_file] = False
    
    # Summary
    print("\n" + "="*60)
    print("COMPILATION SUMMARY")
    print("="*60)
    
    for pipeline_file, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{status}: {pipeline_file}")
    
    # Overall result
    all_success = all(results.values())
    
    print("\n" + "="*60)
    if all_success:
        print("✓ All pipelines compiled successfully!")
        print("="*60)
        print("\nNext steps:")
        print("1. Upload one of the generated YAML files to Kubeflow Pipelines")
        print("2. Create and run a pipeline instance")
        print("3. Monitor execution in the Kubeflow UI")
        print("\nRecommended: Use ml_pipeline.yaml (from pipeline_v2.py)")
        return 0
    else:
        print("✗ Some pipelines failed to compile")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
