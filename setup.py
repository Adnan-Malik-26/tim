#!/usr/bin/env python3
"""Setup script for Tim time tracker."""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

# Read version
version = {}
with open("tim/__init__.py") as fp:
    exec(fp.read(), version)

setup(
    name="tim-tracker",
    version=version["__version__"],
    author="Your Name",
    author_email="your.email@example.com",
    description="A beautiful terminal time tracker with GitHub-style contributions graph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tim",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/tim/issues",
        "Source": "https://github.com/yourusername/tim",
        "Documentation": "https://github.com/yourusername/tim#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Terminals",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
            "twine>=4.0.0",
            "build>=0.10.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "freezegun>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tim=tim.cli:app",
        ],
    },
    keywords="time tracker, productivity, cli, terminal, pomodoro, time management",
    include_package_data=True,
    zip_safe=False,
)
