from setuptools import setup, find_packages

setup(
    name="educhain",
    version="0.3.7",
    packages=find_packages(),
    install_requires=[
        "langchain==0.3.19",
        "langchain-community==0.3.18",
        "langchain-openai==0.3.7",
        "openai==1.64.0",
        "python-dotenv==1.0.1", 
        "reportlab==4.3.1",
        "PyPDF2",
        "beautifulsoup4",
        "youtube-transcript-api==0.6.3",
        "pydantic==2.10.6",
        "requests",
        "chromadb==0.6.3",
        "protobuf<5",
        "pillow", 
        "dataframe-image==0.2.7",
        "langchain-google-genai==2.0.9",
        "pandas",
        "ipython",
        "matplotlib",
        "numpy",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
        ],
    },
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires='>=3.9',
)

