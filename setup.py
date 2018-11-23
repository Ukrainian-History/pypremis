from setuptools import setup

setup(
    name = 'pypremis',
    version = '1.0.1b',
    url = 'https://github.com/bnbalsamo/pypremis',
    packages = ['pypremis'],
    description = "A set of python classes for working with PREMIS records.",
    keywords = ["repository", "file-level", "processing", "premis",
                "metadata", "preservation"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    install_requires = [])
