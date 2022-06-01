======================
Components of Crawler
======================

content ...


HTTP Sender
============

*module* smoothcrawler.components.httpio

What are the problems it may face in process of sending HTTP request? It absolutely are
performance and retry mechanism. For the moment, let's only consider about retry mechanism.
It's possible that occur 2 types of failure of sending HTTP request: **raising any exception/error**
or **get a HTTP response without status code 200**. The former one we could implement it via
one feature in another Python package *MultiRunnable* --- *multirunnable.api.retry*.

content ...

HTTP
------

.. autoclass:: smoothcrawler.components.httpio.HTTP
   :inherited-members:


AsyncHTTP
-----------

.. autoclass:: smoothcrawler.components.httpio.AsyncHTTP
   :inherited-members:


HTTP Response Parser
=====================

*module* smoothcrawler.components.data

Introduce what is 'crawler role' ...

content ...

BaseHTTPResponseParser
------------------------

.. autoclass:: smoothcrawler.components.data.BaseHTTPResponseParser
   :members:


BaseAsyncHTTPResponseParser
----------------------------

.. autoclass:: smoothcrawler.components.data.BaseAsyncHTTPResponseParser
   :members:


Data Processing Handler
========================

*module* smoothcrawler.components.data

Introduce what is 'crawler role' ...

content ...

BaseDataHandler
-----------------

.. autoclass:: smoothcrawler.components.data.BaseDataHandler
   :members:


BaseAsyncDataHandler
----------------------

.. autoclass:: smoothcrawler.components.data.BaseAsyncDataHandler
   :members:


Persistence
=============

*module* smoothcrawler.persistence

Introduce what is 'crawler role' ...

content ...

File
-----

content ...


Database
---------

content ...

