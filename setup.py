from setuptools import setup, find_packages

setup(
    name="educhain",
    version="0.4.0",
    packages=find_packages(),
    install_requires=[
        "langchain>=1.0.0",
        "langchain-openai>=1.1.0",
        "langchain-community>=0.4.1",
        "pydantic>=2.0,<3.0",
        "langchain-text-splitters",
        "langchain-google-genai",
        "openai",
        "python-dotenv",
        "reportlab",
        "PyPDF2",
        "beautifulsoup4",
        "youtube-transcript-api",
        "requests",
        "chromadb",
        "protobuf",
        "pillow",
        "dataframe-image",
        "pandas",
        "ipython",
        "matplotlib",
        "numpy",
        "gtts",  # Google Text-to-Speech
        "pydub",  # Audio processing
        "mutagen",  # Audio metadata handling
     
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
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires='>=3.10',
)
