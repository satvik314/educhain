from setuptools import setup, find_packages

setup(
    name="educhain",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-openai",
        "openai",
        "python-dotenv"
    ],
    author="Satvik Paramkusham",
    author_email="satvik@buildfastwithai.com",
    description="A Python package for generating educational content using Generative AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/satvik314/educhain",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
