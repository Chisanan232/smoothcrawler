======================
Components of Crawler
======================

Here are all the components of **crawler role** to let develop implement the detail
what it works in the process. :ref:`As noted above<About>`, there are some different
types of components of **crawler role**:

* HTTP sender
It's responsible of sending HTTP request, it including set cookie, send via proxy, etc.

* HTTP response parser
Parsing the HTTP response to get the target content data.

* Data processing
Data process of the parsed data.

* Persistence
Persist the final data as a file format or into database.

Please refer to :ref:`lanes pool diagram<different components responsible of different task>`
to clear the relation between **components** and **crawler role**.


HTTP Sender
============

.. _API reference: https://multirunnable.readthedocs.io/en/latest/api_references/decorators.html#retry

*module* smoothcrawler.components.httpio

What are the problems it may face in process of sending HTTP request? It absolutely are
performance and retry mechanism. For the moment, let's only consider about retry mechanism.
It's possible that occur 2 types of failure of sending HTTP request: **raising any exception/error**
or **get a HTTP response without status code 200**. The former one we could implement it via
override 4 functions --- *before_request*, *request_done*, *request_fail* and *request_final*.
Its principle is implementing with another Python package *MultiRunnable* --- *multirunnable.api.retry*.
It could refer to the `API reference`_ of it to clear more detail usage.

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

Parsing HTTP response object.

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

Data process of parsed data of HTTP response object.

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

Persist data as one specific file format or into database.

File
-----

content ...


Database
---------

content ...

