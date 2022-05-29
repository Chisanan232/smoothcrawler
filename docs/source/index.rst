.. SmoothCrawler documentation master file, created by
   sphinx-quickstart on Sun Jan 16 21:22:53 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SmoothCrawler's documentation!
=========================================

|python-versions| |release-version| |pypi-version| |license| |codacy-code-quality|

+--------------+---------------------------------+----------------------+
|      OS      |          Building Status        |    Coverage Status   |
+==============+=================================+======================+
|  Linux/MacOS |  |github-actions build-status|  |   |codecov-coverage| |
+--------------+---------------------------------+----------------------+
|    Windows   |     |appveyor build-status|     | |coveralls-coverage| |
+--------------+---------------------------------+----------------------+


*SmoothCrawler* is a Python framework for being faster and easier to build crawler (or be called web spider).
The core concept of its implementation is SoC (Separation of Concerns).


.. toctree::
   :maxdepth: 3
   :caption: General documentation:

   introduction
   installation
   quickly_start


.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   Crawler </api_reference/crawler.rst>
   URL </api_reference/url.rst>
   HTTP Factory </api_reference/http_handler.rst>
   Data Factory </api_reference/data_handler.rst>
   Persistence Factory </api_reference/persistence.rst>



.. |python-versions| image:: https://img.shields.io/pypi/pyversions/smoothcrawler.svg?logo=python&logoColor=FBE072
    :alt: Travis-CI build status
    :target: https://pypi.org/project/smoothcrawler


.. |release-version| image:: https://img.shields.io/github/release/Chisanan232/smoothcrawler.svg?label=Release&logo=github
    :alt: Package release version in GitHub
    :target: https://github.com/Chisanan232/smoothcrawler/releases


.. |pypi-version| image:: https://badge.fury.io/py/SmoothCrawler.svg
    :alt: Package version in PyPi
    :target: https://badge.fury.io/py/SmoothCrawler


.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg?logo=apache
    :alt: License
    :target: https://opensource.org/licenses/Apache-2.0


.. |travis-ci build-status| image:: https://app.travis-ci.com/Chisanan232/smoothcrawler.svg?branch=master
    :alt: Travis-CI building status
    :target: https://app.travis-ci.com/Chisanan232/smoothcrawler


.. |circle-ci build-status| image:: https://circleci.com/gh/Chisanan232/smoothcrawler.svg?style=shield
    :alt: Circle-CI building status
    :target: https://app.circleci.com/pipelines/github/Chisanan232/smoothcrawler


.. |github-actions build-status| image:: https://github.com/Chisanan232/smoothcrawler/actions/workflows/ci-cd-master.yml/badge.svg
    :alt: GitHub-Actions building status
    :target: https://github.com/Chisanan232/smoothcrawler/actions/workflows/ci-cd-master.yml


.. |appveyor build-status| image:: https://ci.appveyor.com/api/projects/status/1eri78jtxvu5r0q2?svg=true
    :alt: AppVeyor building status
    :target: https://ci.appveyor.com/project/Chisanan232/smoothcrawler


.. |codecov-coverage| image:: https://codecov.io/gh/Chisanan232/smoothcrawler/branch/master/graph/badge.svg?token=BTYTU20FBT
    :alt: Test coverage with 'codecov'
    :target: https://codecov.io/gh/Chisanan232/smoothcrawler


.. |coveralls-coverage| image:: https://coveralls.io/repos/github/Chisanan232/smoothcrawler/badge.svg?branch=master
    :alt: Test coverage with 'coveralls'
    :target: https://coveralls.io/github/Chisanan232/smoothcrawler?branch=master


.. |codacy-code-quality| image:: https://app.codacy.com/project/badge/Grade/cf25e1acc34a4c44b6b1ac7084cfe7c5
    :alt: The code quality level with 'codacy'
    :target: https://www.codacy.com/gh/Chisanan232/smoothcrawler/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Chisanan232/smoothcrawler&amp;utm_campaign=Badge_Grade


