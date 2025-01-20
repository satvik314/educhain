from setuptools import setup, find_packages

setup(
    name="educhain",
    version="0.3.4",
    packages=find_packages(),
    install_requires=[
        "langchain==0.3.4",
        "langchain-community==0.3.3",
        "langchain-openai==0.2.11",
        "openai==1.57.0",
        "python-dotenv==1.0.1", 
        "pandas",
        "reportlab==4.2.5",
        "PyPDF2",
        "beautifulsoup4",
        "youtube_transcript_api==0.6.2",
        "pydantic==2.9.2",
        "requests",
        "chromadb==0.5.15",
        "protobuf<5",
        "Pillow"  #image processing
       
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
    ],
    python_requires='>=3.7',
)

