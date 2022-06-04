import setuptools
import os


here = os.path.abspath(os.path.dirname(__file__))

packages = ["smoothcrawler"]

requires = [
    "multipledispatch>=0.6.0",
    "multirunnable>=0.17.0"
]

test_requires = [
    "pytest>=7.0.0",
    "pytest-cov>=3.0.0",
    "pytest-html>=3.1.1",
    "pytest-rerunfailures>=10.2",
    "codecov>=2.1.12",
    "coveralls>=3.3.1",
    "aiohttp>=3.8.1",
    "urllib3>=1.26.8",
    "requests>=2.27.1",
    "beautifulsoup4>=4.10.0",
    "mysql-connector-python>=8.0.28",
]


about = {}
with open(os.path.join(here, "smoothcrawler", "__pkg_info__.py"), "r", encoding="utf-8") as f:
    exec(f.read(), about)


with open("README.md", "r") as fh:
    readme = fh.read()


setuptools.setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=("test", "study", "example")),
    package_dir={"smoothcrawler": "smoothcrawler"},
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
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
    install_requires=requires,
    tests_require=test_requires,
    project_urls={
        "Documentation": "https://smoothcrawler.readthedocs.io",
        "Source": "https://github.com/Chisanan232/smoothcrawler",
    },
)
