import setuptools


with open("README.md", "r") as fh:
    readme = fh.read()

setuptools.setup(
    name="SmoothCrawler",
    version="0.1.0",
    author="Liu, Bryant",
    author_email="chi10211201@cycu.org.tw",
    license="Apache License 2.0",
    description="Build crawler humanly as different roles.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.6',
    install_requires=[
        "multipledispatch==0.6.0",
        "multirunnable==0.16.1"
    ]
)