from setuptools import setup, find_packages

setup(
    name="educhain",
    version="0.2.10",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-community",
        "langchain-openai",
        "openai",
        "python-dotenv", 
        "pandas",
        "reportlab",
        "PyPDF2",
        "beautifulsoup4",
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
