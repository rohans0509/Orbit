from setuptools import setup, find_packages

setup(
    name="Orbit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
    ],
    entry_points={
        'console_scripts': [
            # Define any command line scripts here
        ],
    },
    author="Rohan Sharma",
    author_email="rohansharma0509@gmail.com",
    description="A framework for creating, managing, and executing a chain of agents in a graph-like structure.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/rohans0509/Orbit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
