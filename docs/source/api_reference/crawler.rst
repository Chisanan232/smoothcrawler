=========
Crawlers
=========

*module* smoothcrawler.crawler

Here are the module which has many different **Crawler roles** for different scenarios.
They also are the 'final production' which combines the needed components as web spider
and uses that features.

So **components** implement what it works at each processes, **crawler role** implement
how it works with its components.


Framework Modules
===================

Base Crawler
--------------

.. autoclass:: smoothcrawler.crawler.BaseCrawler
    :private-members: _initial_factory
    :members:


MultiRunnable Crawler
----------------------

.. autoclass:: smoothcrawler.crawler.MultiRunnableCrawler
    :private-members: _get_lock_feature, _divide_urls
    :members:



Implementation Modules
=======================

Simple Crawler
----------------

.. autoclass:: smoothcrawler.crawler.SimpleCrawler
   :inherited-members:


Asynchronous Simple Crawler
----------------------------

.. autoclass:: smoothcrawler.crawler.AsyncSimpleCrawler
   :inherited-members:


Executor Crawler
-----------------

.. autoclass:: smoothcrawler.crawler.ExecutorCrawler
   :inherited-members:


Pool Crawler
-------------

.. autoclass:: smoothcrawler.crawler.PoolCrawler
   :inherited-members:



