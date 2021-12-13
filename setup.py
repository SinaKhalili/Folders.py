import os
from setuptools import setup

version = "0.0.5"
long_description = open(f"README.md").read()


setup(
    name="Folders",
    version=version,
    author="Sina Khalili",
    author_email="khalili@sfu.ca",
    url="https://github.com/SinaKhalili/Folders.py",
    description="Implementation of the Folders📂 esoteric programming language, a language with no code and just folders.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    
    entry_points={"console_scripts": ["Folders = folders:main"]},
)
