# SmoothCrawler

[![Supported Versions](https://img.shields.io/pypi/pyversions/smoothcrawler.svg?logo=python&logoColor=FBE072)](https://pypi.org/project/smoothcrawler)
[![Release](https://img.shields.io/github/release/Chisanan232/smoothcrawler.svg?label=Release&sort=semver)](https://github.com/Chisanan232/smoothcrawler/releases)
[![PyPI version](https://badge.fury.io/py/SmoothCrawler.svg)](https://badge.fury.io/py/SmoothCrawler)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

| OS | Building Status | Coverage Status |
|------------|------------|--------|
| Linux |[![Build Status](https://app.travis-ci.com/Chisanan232/smoothcrawler.svg?branch=master)](https://app.travis-ci.com/Chisanan232/smoothcrawler)|Deprecated|
| Linux |[![CircleCI](https://circleci.com/gh/Chisanan232/smoothcrawler.svg?style=shield)](https://app.circleci.com/pipelines/github/Chisanan232/smoothcrawler)|[![codecov](https://codecov.io/gh/Chisanan232/smoothcrawler/branch/master/graph/badge.svg?token=BTYTU20FBT)](https://codecov.io/gh/Chisanan232/smoothcrawler)|
| Linux/MacOS |[![Run Python Tests](https://github.com/Chisanan232/smoothcrawler/actions/workflows/ci.yml/badge.svg)](https://github.com/Chisanan232/smoothcrawler/actions/workflows/ci.yml)|[![codecov](https://codecov.io/gh/Chisanan232/smoothcrawler/branch/master/graph/badge.svg?token=BTYTU20FBT)](https://codecov.io/gh/Chisanan232/smoothcrawler)|
| Windows |[![Build status](https://ci.appveyor.com/api/projects/status/1eri78jtxvu5r0q2?svg=true)](https://ci.appveyor.com/project/Chisanan232/smoothcrawler)|[![Coverage Status](https://coveralls.io/repos/github/Chisanan232/smoothcrawler/badge.svg?branch=master)](https://coveralls.io/github/Chisanan232/smoothcrawler?branch=master)|

A Python package for building crawler humanly as different roles.

[Overview](#overview) | [Quickly Start](#quickly-start) | [Code Example](https://github.com/Chisanan232/smoothcrawler/tree/master/example)
<hr>


## Overview

Implementing web crawler in Python is very easy and simple. It already has many frameworks or libraries to do it.
However, they focus on one point. It means that they all have their own responsibility to face different things.
For HTTP, you must think about *urllib3* or *requests*; For parsing HTTP response, *Beautiful Soup*. A framework to do it, *scrapy* or *selenium*.
How about a library to build a **crawler system**?

Every crawler should do mostly same things and procedures:

    send HTTP request -> get HTTP response and parse it -> handle data if it's necessary -> persistence process

In general, a crawler code usually be used 1 or 2 times. It even could implement and run the code via writing script. 
That's the reason why it doesn't need to develop a **program** for crawler, much less maintain the crawler program (for example, web element locations will be your nightmare) or change requirement.

_smoothcrawler_ like LEGO blocks, it classifies crawling to be some components. Every component has its own responsibility to do something. 
Components could reuse others if it needs. One component focus one thing. Finally, the components combines to form a crawler.


## Quickly Start

Install _smoothcrawler_ via **pip**:

    pip install smoothcrawler

Let's write a simple crawler to crawl data.

* Component 1: Send HTTP requests

Implement with Python package _urllib3_. Of course, it could implement by _requests_, too.

```python
from smoothcrawler.components.httpio import HTTP
import urllib3

class FooHTTPRequest(HTTP):

    __Http_Response = None

    def get(self, url: str, *args, **kwargs):
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("GET", url)
        return self.__Http_Response
```

* Component 2: Get and parse HTTP response

Get the HTTP response object and get the content data from it. It only decodes the data because the data is so clean of the API.

```python
from smoothcrawler.components.data import BaseHTTPResponseParser
from typing import Any
import urllib3

class FooHTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self, response: urllib3.response.HTTPResponse) -> int:
        return response.status


    def handling_200_response(self, response: urllib3.response.HTTPResponse) -> Any:
        _data = response.data.decode('utf-8')
        return _data
```

* Component 3: Handle data processing

Demonstrate it could do some data processing here.

```python
from smoothcrawler.components.data import BaseDataHandler
import json

class FooDataHandler(BaseDataHandler):

    def process(self, result):
        _result_json = json.loads(result)
        _result_data = _result_json["data"]

        _final_data = []
        _data_row = []

        for _d in _result_data:
            # # stock_date
            _data_row.append(_d[0].replace("/", "-"))
            # # trade_volume
            _data_row.append(int(_d[1].replace(",", "")))
            # # turnover_price
            _data_row.append(int(_d[2].replace(",", "")))
            # # opening_price
            _data_row.append(float(_d[3]))
            # # highest_price
            _data_row.append(float(_d[4]))
            # # lowest_price
            _data_row.append(float(_d[5]))
            # # closing_price
            _data_row.append(float(_d[6]))
            # # gross_spread
            _data_row.append(str(_d[7]))
            # # turnover_volume
            _data_row.append(int(_d[8].replace(",", "")))

            _final_data.append(_data_row.copy())
            _data_row[:] = []

        return _final_data
```

* Product: Components combine to form a  crawler

It has 3 components now: HTTP sender, HTTP response parser and data processing handler.
They could combine to form a crawler and crawl data from target URL(s) via crawler role 'SimpleCrawler'.

```python
from smoothcrawler.crawler import SimpleCrawler
from smoothcrawler.factory import CrawlerFactory

# Taiwan stock data
Test_URL_TW_Stock = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210801&stockNo=2330"

_cf = CrawlerFactory()
_cf.http_factory = FooHTTPRequest()
_cf.parser_factory = FooHTTPResponseParser()
_cf.data_handling_factory = FooDataHandler()

# Crawler Role: Simple Crawler
sc = SimpleCrawler(factory=_cf)
data = sc.run("GET", Test_URL_TW_Stock)
print(f"data: {data}")
```

