=============
Installation
=============

Install by pip
===============

To install *SmoothCrawler*, it's easy to install via command with tool *pip*:

.. code-block:: shell

    >>> pip install smoothcrawler


Dependencies
==============

.. _here: https://multirunnable.readthedocs.io/en/latest/

* *multirunnable*: The documentation of *MultiRunnable* is `here`_.

*SmoothCrawler* also provides 2 types of crawler --- *ExecutorCrawler* and *PoolCrawler*.
Developer could easily implement web spider parallelism with them. The principle of them
is it implements parallelism with another Python library --- *MultiRunnable*. So
*MultiRunnable* is the necessary dependency of *SmoothCrawler*.


Related Dependencies in usage with SmoothCrawler
=================================================

From the :ref:`key point<About Important>` of *SmoothCrawler*. It already be known that
*SmoothCrawler* is a framework, isn't an implementation. It provides software architecture
to let you follow, but the detail how it works is your task. Hence, it always works with some
libraries like below:

* *urllib3*
* *requests*
* *aiohttp*
* *beautifulsoup*

Some of them (*urllib3*, *requests*, *aiohttp*) are responsible for sending HTTP request,
one of them (*beautifulsoup*) is responsible for parsing HTTP response. Except for them,
it must has other libraries to do something which could be applied in components of
*SmoothCrawler*. They're just examples which is the mostly be used.

