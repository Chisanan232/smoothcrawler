# smoothcrawler

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Release](https://img.shields.io/github/release/Chisanan232/smoothcrawler.svg?label=Release&sort=semver)](https://github.com/Chisanan232/smoothcrawler/releases)
[![PyPI version](https://badge.fury.io/py/smoothcrawler.svg)](https://badge.fury.io/py/smoothcrawler)
[![Supported Versions](https://img.shields.io/pypi/pyversions/smoothcrawler.svg?logo=python&logoColor=FBE072)](https://pypi.org/project/smoothcrawler)
[![Coverage Status](https://coveralls.io/repos/github/Chisanan232/smoothcrawler/badge.svg)](https://coveralls.io/github/Chisanan232/smoothcrawler)
[![codecov](https://codecov.io/gh/Chisanan232/smoothcrawler/branch/master/graph/badge.svg?token=BTYTU20FBT)](https://codecov.io/gh/Chisanan232/smoothcrawler)

| Linux/MacOS | Windows |
|------------|--------|
|[![Build Status](https://app.travis-ci.com/Chisanan232/smoothcrawler.svg?branch=master)](https://app.travis-ci.com/Chisanan232/smoothcrawler)|[![Build status](https://ci.appveyor.com/api/projects/status/1eri78jtxvu5r0q2?svg=true)](https://ci.appveyor.com/project/Chisanan232/smoothcrawler)|

A Python package for building software architecture of crawler humanly.
<hr>

[Overview](#overview) | [Quickly Start](#quickly-start) | [Flow](#flow) | [Usage](#usage) | [Code Example](https://github.com/Chisanan232/smoothcrawler/tree/master/example)
<hr>


## Overview

Implementing web crawler in Python is very easy and simple. It already has many frameworks or libraries to do it.
However, they focus on one point. It means that they have their responsibility to face different things.
For HTTP, you must think about *urllib* or *requests*; For parsing HTTP response, *Beautiful Soup*. A framework to do it, *scrapy* or *selenium*.
How about a library to build a crawler **software architecture**?
Think about it, every crawler should do mostly same things and procedures:

    send HTTP request -> get HTTP response and parse it -> handle data if it's needed -> persistence process

It could implement and run a crawler via writing script, doesn't need to develop a **program**.
Of course, it can do that. Sometimes, it just is needed once so that it's not necessary to thinking more and more concerns like maintaining, extending or something else.


## Quickly Start

This package doesn't release currently. So it only could be installed by _setup.py_.

    python setup.py install

Let's write a simple crawler to crawl data.


## Flow

* ### Work Flow

The work-flow about crawling target web content: <br>
<img src="https://github.com/Chisanan232/pytsunami/blob/master/doc/imgs/SmoothCrawler-Work_Flow.png" width="461" height="681" alt="Crawler work-flow"/><br/>


* ### Cross Function Flow
<img src="https://github.com/Chisanan232/smoothcrawler/blob/master/doc/imgs/smoothcrawler_simple-crawler_cross-function_flow.png" width="725" height="700" alt="Crawler work-flow"/><br/>


## Usage

* Crawler Roles
    * [Simple Crawler](#simple-crawler)
    * [Executor Crawler](#executor-crawler)
    * [Asynchronous Executor Crawler](#asynchronous-executor-crawler)
    * [Pool Crawler](#pool-crawler)
    * [Crazy Crawler](#crazy-crawler)
* Crawler Components
    * [HTTP IO Handler](#http-io-handler)
    * [Data Handler](#data-handler)
        * [HTTP Response](#http-response)
        * [Data Process](#data-process)
    * [Persistence Handler](#persistence-handler)
        * [File](#file)
        * [Database](#database)

<br>

### Crawler Roles
<hr>

* ### Simple Crawler

* ### Executor Crawler

* ### Asynchronous Executor Crawler

* ### Pool Crawler

* ### Crazy Crawler

<br>


### Crawler Components
<hr>

* ### HTTP IO Handler

* ### Data Handler

    * #### HTTP Response

    * #### Data Process

* ### Persistence Handler

    * #### File

    * #### Database



