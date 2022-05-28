=========
Crawlers
=========

*module* smoothcrawler.crawler

Introduce what is 'crawler role' ...


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
    :private-members: _initial_factory
   :inherited-members:


Executor Crawler
-----------------

.. autoclass:: smoothcrawler.crawler.ExecutorCrawler
   :inherited-members:


Pool Crawler
-------------

.. autoclass:: smoothcrawler.crawler.PoolCrawler
   :inherited-members:



