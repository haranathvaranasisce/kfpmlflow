"""
Setup script for the kfpmlflow package.
This makes the common module accessible to all pipeline components at runtime.
"""

from setuptools import setup, find_packages

setup(
    name="kfpmlflow",
    version="0.1.0",
    description="KFP V2 ML Pipeline with shared commons module",
    author="Your Name",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "kfp>=2.5.0",
        "pandas>=2.0.3",
        "scikit-learn>=1.3.0",
        "numpy>=1.24.3",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
