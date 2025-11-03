#!/usr/bin/env python3
"""
Setup configuration for XMind Converter package.
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="xmind-converter",
    version="1.0.0",
    author="MarlinZH",
    description="Convert XMind mind maps to various formats (Markdown, CSV, Notion, Neo4j)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarlinZH/xmind_converter",
    packages=find_packages(exclude=["tests", "tests.*", "config"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "xmindparser>=1.0.8",
        "pandas>=2.0.0",
        "notion-client>=2.2.0",
        "neo4j>=5.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "xmind-convert=xmind_converter.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
