#!/usr/bin/env python3
"""
Marketing Automation System Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="marketing-automation-system",
    version="1.0.0",
    author="ChadTech Industries",
    author_email="dev@chadtech.com",
    description="Automated marketing system for mobile apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chadtech/marketing-automation-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-mock>=3.10.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "dashboard": [
            "streamlit>=1.28.0",
            "plotly>=5.15.0",
            "altair>=5.0.0",
        ],
        "ai": [
            "openai>=1.0.0",
            "anthropic>=0.5.0",
            "replicate>=0.15.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "marketing-automation=marketing_orchestrator:main",
            "marketing-dashboard=start_dashboard:main",
            "aso-optimizer=aso.keyword_optimizer:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.yaml", "*.yml", "*.txt", "*.md"],
    },
    project_urls={
        "Bug Reports": "https://github.com/chadtech/marketing-automation-system/issues",
        "Source": "https://github.com/chadtech/marketing-automation-system",
        "Documentation": "https://marketing-automation-docs.chadtech.com",
    },
)