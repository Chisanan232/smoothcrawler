# SmoothCrawler

[![Supported Versions](https://img.shields.io/pypi/pyversions/smoothcrawler.svg?logo=python&logoColor=FBE072)](https://pypi.org/project/smoothcrawler)
[![Release](https://img.shields.io/github/release/Chisanan232/SmoothCrawler.svg?label=Release&logo=github)](https://github.com/Chisanan232/SmoothCrawler/releases)
[![PyPI version](https://badge.fury.io/py/SmoothCrawler.svg?logo=pypi)](https://badge.fury.io/py/SmoothCrawler)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg?logo=apache)](https://opensource.org/licenses/Apache-2.0)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cf25e1acc34a4c44b6b1ac7084cfe7c5)](https://www.codacy.com/gh/Chisanan232/smoothcrawler/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Chisanan232/smoothcrawler&amp;utm_campaign=Badge_Grade)
[![Documentation Status](https://readthedocs.org/projects/smoothcrawler/badge/?version=latest)](https://smoothcrawler.readthedocs.io/en/latest/?badge=latest)

| OS | Building Status | Coverage Status |
|------------|------------|--------|
| Linux/MacOS |[![SmoothCrawler CI/CD](https://github.com/Chisanan232/smoothcrawler/actions/workflows/ci-cd-master.yml/badge.svg)](https://github.com/Chisanan232/smoothcrawler/actions/workflows/ci-cd-master.yml)|[![codecov](https://codecov.io/gh/Chisanan232/smoothcrawler/branch/master/graph/badge.svg?token=BTYTU20FBT)](https://codecov.io/gh/Chisanan232/smoothcrawler)|
| Windows |[![Build status](https://ci.appveyor.com/api/projects/status/1eri78jtxvu5r0q2?svg=true)](https://ci.appveyor.com/project/Chisanan232/smoothcrawler)|[![Coverage Status](https://coveralls.io/repos/github/Chisanan232/smoothcrawler/badge.svg?branch=master)](https://coveralls.io/github/Chisanan232/smoothcrawler?branch=master)|

[comment]: <> (| Linux |[![Build Status]&#40;https://app.travis-ci.com/Chisanan232/smoothcrawler.svg?branch=master&#41;]&#40;https://app.travis-ci.com/Chisanan232/smoothcrawler&#41;|Deprecated|)

[comment]: <> (| Linux |[![CircleCI]&#40;https://circleci.com/gh/Chisanan232/smoothcrawler.svg?style=shield&#41;]&#40;https://app.circleci.com/pipelines/github/Chisanan232/smoothcrawler&#41;|[![codecov]&#40;https://codecov.io/gh/Chisanan232/smoothcrawler/branch/master/graph/badge.svg?token=BTYTU20FBT&#41;]&#40;https://codecov.io/gh/Chisanan232/smoothcrawler&#41;|)

*SmoothCrawler* is a Python framework for being faster and easier to build crawler (or be called web spider).
The core concept of its implementation is SoC (Separation of Concerns). It could build crawler humanly as different 
roles which be combined with different components.

[Overview](#overview) | [Quickly Demo](#quickly-demo) | [Documentation](#documentation)  | [Code Example](https://github.com/Chisanan232/smoothcrawler/tree/master/example)
<hr>


## Overview

Implementing a web crawler in Python is very easy and simple. It already has many frameworks or libraries to do it.
However, they focus on one point. It means that they all have their own responsibility to face different things:

* For HTTP, you must think about *urllib3* or *requests*.
* For parsing HTTP response, *BeautifulSoup* (*bs4*).
* A framework to do it, *scrapy* or *selenium*.

How about a library to build a **crawler system**?

Every crawler should do mostly same things and procedures:

![image](https://github.com/Chisanan232/smoothcrawler/blob/master/docs/source/images/work_flow/Work_Process(Briefly).drawio.png)

In generally, a crawler code usually be unstable and even be difficult (e.g. parsing a complex HTML elements content). 
So it's keeping facing many challenges when you're developing web spider, much less maintain the crawler program (for 
example, web element locations changing will be your nightmare) or change requirement.

_smoothcrawler_ like LEGO blocks, it classifies crawling to be some components. Every component has its own responsibility to do something. 
Components could reuse others if it needs. One component focus one thing. Finally, the components combines to form a crawler.


## Quickly Demo

Install _smoothcrawler_ via **pip**:

    pip install smoothcrawler

Let's write a simple crawler to crawl data.

* Component 1: Send HTTP requests

Implement with Python package _requests_. Of course, it could implement by _urllib3_, too.

```python
from smoothcrawler.components.httpio import HTTP
import requests

class FooHTTPRequest(HTTP):

    __Http_Response = None

    def get(self, url: str, *args, **kwargs):
            self.__Http_Response = requests.get(url)
            return self.__Http_Response
```

* Component 2: Get and parse HTTP response

Get the HTTP response object and parse the content data from it.

```python
from smoothcrawler.components.data import BaseHTTPResponseParser
from bs4 import BeautifulSoup
import requests


class FooHTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self, response: requests.Response) -> int:
        return response.status

    def handling_200_response(self, response: requests.Response) -> str:
        _bs = BeautifulSoup(response.text, "html.parser")
        _example_web_title = _bs.find_all("h1")
        return _example_web_title[0].text
```

* Component 3: Handle data processing

Demonstrate it could do some data processing here.

```python
from smoothcrawler.components.data import BaseDataHandler

class FooDataHandler(BaseDataHandler):

    def process(self, result):
        return "This is the example.com website header text: " + result
```

* Product: Components combine to form a  crawler

It has 3 components now: HTTP sender, HTTP response parser and data processing handler.
They could combine to form a crawler and crawl data from target URL(s) via crawler role _SimpleCrawler_.

```python
from smoothcrawler.crawler import SimpleCrawler
from smoothcrawler.factory import CrawlerFactory

_cf = CrawlerFactory()
_cf.http_factory = FooHTTPRequest()
_cf.parser_factory = FooHTTPResponseParser()
_cf.data_handling_factory = FooDataHandler()

# Crawler Role: Simple Crawler
sc = SimpleCrawler(factory=_cf)
data = sc.run("GET", "http://www.example.com")
print(data)
# This is the example.com website header text: Example Domain
```

* Be more easier implementation in one object.

You may think: come on, I just want to get a simple data easily, so I don't want to 
divergent simple implementations to many different objects. It's not clear and graceful.

Don't worry, it also could implement that in one object which extends _SimpleCrawler_ like following:

```python
from smoothcrawler.crawler import SimpleCrawler
from bs4 import BeautifulSoup
import requests

class ExampleEasyCrawler(SimpleCrawler):

   def send_http_request(self, method: str, url: str, retry: int = 1, *args, **kwargs) -> requests.Response:
       _response = requests.get(url)
       return _response


   def parse_http_response(self, response: requests.Response) -> str:
       _bs = BeautifulSoup(response.text, "html.parser")
       _example_web_title = _bs.find_all("h1")
       return _example_web_title[0].text


   def data_process(self, parsed_response: str) -> str:
       return "This is the example.com website header text: " + parsed_response
```

Finally, you could instantiate and use it directly:

```python
_example_easy_crawler = ExampleEasyCrawler()    # Instantiate your own crawler object
_example_result = _example_easy_crawler.run("get", "http://www.example.com")    # Run the web spider task with function *run* and get the result
print(_example_result)
# This is the example.com website header text: Example Domain
```

How the usage easy and code clear is!


## Documentation

The [documentation](https://smoothcrawler.readthedocs.io) contains more details, and examples.

* [Quickly Start](https://smoothcrawler.readthedocs.io/en/latest/quickly_start.html) to develop web spider with *SmoothCrawler*


## Download 

*SmoothCrawler* still a young open source which keep growing. Here's its download state: 

[![Downloads](https://pepy.tech/badge/smoothcrawler)](https://pepy.tech/project/smoothcrawler)
[![Downloads](https://pepy.tech/badge/smoothcrawler/month)](https://pepy.tech/project/smoothcrawler)
