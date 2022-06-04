=========
Factory
=========

The *Factory* object saves each components instance as its properties. And it's necessary
that pass factory object into *Crawler* object. It would provide each components *Crawler*
object needs to use in process.

But in version 0.2.0, it also could register components instance via function *register_factory*
of *Crawler* object.

Please refer these 2 ways usage as following:

* Pass *Factory* which saves components into *Crawler* by option *factory*

First of all, instantiate components and save it as factory object's properties:

.. code-block:: python

    _cf = CrawlerFactory()
    _cf.http_factory = YourHTTPRequest()
    _cf.parser_factory = YourHTTPResponseParser()
    _cf.data_handling_factory = YourDataHandler()

Pass the *CrawlerFactory* as option *factory* and run it via function *run*:

.. code-block:: python

    sc = SimpleCrawler(factory=_cf)
    data = sc.run("GET", "http://www.example.com/")
    print(f"[DEBUG] data: {data}")
    # [DEBUG] data: Example Domain


* Register components to *Crawler* by function *register_factory*

Register the factories via function *register_factory* and run it:

.. code-block:: python

    sc = SimpleCrawler(factory=_cf)
    sc.register_factory(
        http_req_sender=RequestsHTTPRequest(),
        http_resp_parser=RequestsExampleHTTPResponseParser(),
        data_process=ExampleDataHandler()
    )

    data = sc.run("GET", "http://www.example.com/")
    print(f"[DEBUG] data: {data}")
    # [DEBUG] data: Example Domain


CrawlerFactory
---------------

.. autoclass:: smoothcrawler.factory.CrawlerFactory
   :members:


AsyncCrawlerFactory
--------------------

.. autoclass:: smoothcrawler.factory.AsyncCrawlerFactory
   :members:

