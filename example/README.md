# Example Code with '_smoothcrawler_'

Here are some example code about how to use this package.

[Environment](#environment)

## Environment
<hr>

[![Supported Versions](https://img.shields.io/pypi/pyversions/smoothcrawler.svg?logo=python&logoColor=FBE072)](https://pypi.org/project/smoothcrawler)

Installation by pip:

    pip install smoothcrawler

It also could run in virtual environment like _virtualenv_ or Docker. 
It's better to clear your own develop environment.

* Python Virtual Environment

Please install virtualenv first:

    pip install virtualenv -U

Initial a Python virtual environment with target directory:

    virtualenv -p python3 ./package_test_env

Activate and switch to the environment:

    source ./package_test_env/bin/activate

Finally, we could install the package and do something with it. <br>
Remember, this is a new environment, so it absolutely doesn't have the packages it has outside.
You could leave it by command _deactivate_:

    deactivate


* Docker

First of all, make sure that Docker has already:

    docker --version

> ⚠️ Remember: It's not necessary about preparing Python environment with Docker.

You also could verify its brief:

    docker info

Everything is ready, let's start to build image:

    docker build -t smoothcrawler_client:py37 ./ -f ./Dockerfile_py37

Verify it:

    docker images | grep -E "smoothcrawler_client"

Run it:

    docker run --name smoothcrawler_executor_client_py37 smoothcrawler_client:py37

