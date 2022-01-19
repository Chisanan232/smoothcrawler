import pytest

from smoothcrawler.factory import CrawlerFactory, AsyncCrawlerFactory

from ._components import (
    MyRetry,
    StockHTTPRequest, StockAsyncHTTPRequest,
    StockHTTPResponseParser, StockAsyncHTTPResponseParser,
    StockDataHandler, StockAsyncDataHandler,
    StockDataFilePersistenceLayer,
    StockDataDatabasePersistenceLayer)


@pytest.fixture(scope="function")
def crawler_factory() -> CrawlerFactory:
    return CrawlerFactory()


@pytest.fixture(scope="function")
def async_crawler_factory() -> AsyncCrawlerFactory:
    return AsyncCrawlerFactory()


class TestCrawlerFactory:

    def test_http_factory(self, crawler_factory: CrawlerFactory):
        _http_req = StockHTTPRequest(retry_components=MyRetry())

        try:
            crawler_factory.http_factory = _http_req
        except Exception as e:
            assert False, f"It should set the factory via property finely."
        else:
            assert True, f"It works."

            assert crawler_factory.http_factory == _http_req, f"Property value should be equal to the instance."


    def test_parser_factory(self, crawler_factory: CrawlerFactory):
        _response_parser = StockHTTPResponseParser()

        try:
            crawler_factory.parser_factory = _response_parser
        except Exception as e:
            assert False, f"It should set the factory via property finely."
        else:
            assert True, f"It works."

            assert crawler_factory.parser_factory == _response_parser, f"Property value should be equal to the instance."


    def test_data_handling_factory(self, crawler_factory: CrawlerFactory):
        _data_handler = StockDataHandler()

        try:
            crawler_factory.data_handling_factory = _data_handler
        except Exception as e:
            assert False, f"It should set the factory via property finely."
        else:
            assert True, f"It works."

            assert crawler_factory.data_handling_factory == _data_handler, f"Property value should be equal to the instance."


    def test_persistence_factory(self, crawler_factory: CrawlerFactory):
        _persistence_handler = StockDataFilePersistenceLayer()

        try:
            crawler_factory.persistence_factory = _persistence_handler
        except Exception as e:
            assert False, f"It should set the factory via property finely."
        else:
            assert True, f"It works."

            assert crawler_factory.persistence_factory == _persistence_handler, f"Property value should be equal to the instance."


class TestAsyncCrawlerFactory:

    def test_http_factory(self, async_crawler_factory: CrawlerFactory):
        _http_req = StockAsyncHTTPRequest()

        try:
            async_crawler_factory.http_factory = _http_req
        except Exception as e:
            assert False, f"It should set the factory via property finely."
        else:
            assert True, f"It works."

            assert async_crawler_factory.http_factory == _http_req, f"Property value should be equal to the instance."


    def test_parser_factory(self, async_crawler_factory: CrawlerFactory):
        _response_parser = StockAsyncHTTPResponseParser()

        try:
            async_crawler_factory.parser_factory = _response_parser
        except Exception as e:
            assert False, f"It should set the factory via property finely."
        else:
            assert True, f"It works."

            assert async_crawler_factory.parser_factory == _response_parser, f"Property value should be equal to the instance."


    def test_data_handling_factory(self, async_crawler_factory: CrawlerFactory):
        _data_handler = StockAsyncDataHandler()

        try:
            async_crawler_factory.data_handling_factory = _data_handler
        except Exception as e:
            assert False, f"It should set the factory via property finely."
        else:
            assert True, f"It works."

            assert async_crawler_factory.data_handling_factory == _data_handler, f"Property value should be equal to the instance."


    def test_persistence_factory(self, async_crawler_factory: CrawlerFactory):
        _persistence_handler = StockDataFilePersistenceLayer()

        try:
            async_crawler_factory.persistence_factory = _persistence_handler
        except Exception as e:
            assert False, f"It should set the factory via property finely."
        else:
            assert True, f"It works."

            assert async_crawler_factory.persistence_factory == _persistence_handler, f"Property value should be equal to the instance."

