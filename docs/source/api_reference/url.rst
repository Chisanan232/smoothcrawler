=====
URL
=====

Before it runs web spider tasks, it must to prepare all the URLs. It's very various.
It maybe have option, for examples, date or datetime, unix time, some specific index, ect.
This module target to handle and generate the URLs to let web spider to use.

.. autodata:: smoothcrawler.urls.OPTION_VAR_INDEX

*URL* object could generate URLs with index (0, 1, 2 ...) by iterator.

.. code-block:: python

    from smoothcrawler.urls import URL, OPTION_VAR_INDEX

    _target_url = "http:www.test.com?index={" + OPTION_VAR_INDEX + "}"
    _index_urls = URL(_target_url, start=0, end=5)
    _urls = _index_urls.generate()
    print(_urls)
    # ['http:www.test.com?index=0', 'http:www.test.com?index=1', 'http:www.test.com?index=2', 'http:www.test.com?index=3', 'http:www.test.com?index=4', 'http:www.test.com?index=5']


.. autodata:: smoothcrawler.urls.OPTION_VAR_DATE

*URL* object could generate URLs with date by iterator. It could set the format to let it generates URL via date value with its format.

.. code-block:: python

    from smoothcrawler.urls import URL, OPTION_VAR_DATE

    _target_url = "http:www.test.com?date={" + OPTION_VAR_DATE + "}"
    _date_urls = URL(_target_url, start="20220601", end="20220603", formatter="yyyymmdd")
    _urls = _date_urls.generate()
    print(_urls)
    # ['http:www.test.com?date=20220601', 'http:www.test.com?date=20220602', 'http:www.test.com?date=20220603']


.. autodata:: smoothcrawler.urls.OPTION_VAR_DATETIME

*URL* object could generate URLs with datetime by iterator. It could set the format to let it generates URL via datetime value with its format.

.. code-block:: python

    from smoothcrawler.urls import URL, OPTION_VAR_DATETIME

    _target_url = "http:www.test.com?datetime={" + OPTION_VAR_DATETIME + "}"
    _datetime_urls = URL(_target_url, start="2022/06/01 00:00:00", end="2022/06/03 00:00:00", formatter="yyyy/mm/dd HH:MM:SS")
    _urls = _datetime_urls.generate()
    print(_urls)
    # ['http:www.test.com?datetime=20220601000000', 'http:www.test.com?datetime=20220602000000', 'http:www.test.com?datetime=20220603000000']


.. autodata:: smoothcrawler.urls.OPTION_VAR_ITERATOR

*URL* object could generate URLs with one specific iterator object.

.. code-block:: python

    from smoothcrawler.urls import URL, OPTION_VAR_ITERATOR

    _target_url = "http:www.test.com?index_with_iter={" + OPTION_VAR_ITERATOR + "}"
    _iter_urls = URL(_target_url, iter=[i for i in range(1, 4)])
    _urls = _iter_urls.generate()
    print(_urls)
    # ['http:www.test.com?index_with_iter=1', 'http:www.test.com?index_with_iter=2', 'http:www.test.com?index_with_iter=3']


.. autofunction:: smoothcrawler.urls.get_option
.. autofunction:: smoothcrawler.urls.set_index_rule
.. autofunction:: smoothcrawler.urls.set_date_rule
.. autofunction:: smoothcrawler.urls.set_datetime_rule
.. autofunction:: smoothcrawler.urls.set_iterator_rule


URL
====

.. autoclass:: smoothcrawler.urls.URL
    :private-members: _index_handling, _is_py_datetime_format, _convert_formatter, _date_handling, _datetime_handling, _iterator_handling, _add_flag
    :members:
