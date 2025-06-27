#!/usr/bin/env python3
"""
Setup script for CMOS Inverter Simulation
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cmos-inverter-simulation",
    version="2.0.0",
    author="Zeyad Mustafa",
    author_email="your.email@example.com",
    description="Advanced CMOS Inverter Simulation with comprehensive analysis capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zeyad-Mustafa/CMOS-Inverter-Simulation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Topic :: Education",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="CMOS, inverter, simulation, VLSI, electronics, semiconductor",
    project_urls={
        "Bug Reports": "https://github.com/Zeyad-Mustafa/CMOS-Inverter-Simulation/issues",
        "Source": "https://github.com/Zeyad-Mustafa/CMOS-Inverter-Simulation",
    },
)