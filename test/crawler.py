from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic
import pytest

from smoothcrawler.crawler import BaseCrawler, SimpleCrawler, AsyncSimpleCrawler, ExecutorCrawler, PoolCrawler, RunningMode
from smoothcrawler.urls import URL
from smoothcrawler.factory import CrawlerFactory

from ._components import (
    MyRetry,
    StockHTTPRequest,
    StockHTTPResponseParser,
    StockDataHandler,
    StockDataFilePersistenceLayer,
    StockDataDatabasePersistenceLayer)


T = TypeVar("T")

HTTP_METHOD = "GET"
TEST_URL = "https://www.google.com"
TEST_TIMEOUT_URL = "https://www.test.com"
Test_URL_TW_Stock = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210801&stockNo=2330"
Test_URL_TW_Stock_With_Option = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date={date}&stockNo=2330"



class BaseCrawlerTestSpec(metaclass=ABCMeta):

    """
    Test cases:
        Test for the crawler. I think it should attach important to the
        crawling procedure or the return value of factories.
    """

    @pytest.fixture
    @abstractmethod
    def crawler(self) -> BaseCrawler:
        pass


    @abstractmethod
    def test_run(self, crawler: Generic[T]):
        pass



class TestSimpleCrawler(BaseCrawlerTestSpec):

    @pytest.fixture
    def crawler(self) -> BaseCrawler:
        _cf = CrawlerFactory()
        _cf.http_factory = StockHTTPRequest(retry_components=MyRetry())
        _cf.parser_factory = StockHTTPResponseParser()
        _cf.data_handling_factory = StockDataHandler()

        _sc = SimpleCrawler(factory=_cf)
        return _sc


    def test_run(self, crawler: SimpleCrawler):
        result = crawler.run("GET", Test_URL_TW_Stock)
        assert result is not None, f"It should get some data finally."



class TestAsyncSimpleCrawler(BaseCrawlerTestSpec):

    @pytest.fixture
    def crawler(self) -> BaseCrawler:
        _cf = CrawlerFactory()
        _cf.http_factory = StockHTTPRequest(retry_components=MyRetry())
        _cf.parser_factory = StockHTTPResponseParser()
        _cf.data_handling_factory = StockDataHandler()

        _sc = AsyncSimpleCrawler(factory=_cf, executors=3)
        return _sc


    @pytest.mark.skip(reason="")
    def test_factory(self, crawler: Generic[T]):
        pass


    @pytest.mark.skip(reason="[AsyncSimpleCrawler] It doesn't finish testing logic.")
    def test_run(self, crawler: AsyncSimpleCrawler):
        result = crawler.run()



class TestExecutorCrawler(BaseCrawlerTestSpec):

    @pytest.fixture
    def crawler(self) -> BaseCrawler:
        _cf = CrawlerFactory()
        _cf.http_factory = StockHTTPRequest(retry_components=MyRetry())
        _cf.parser_factory = StockHTTPResponseParser()
        _cf.data_handling_factory = StockDataHandler()

        _sc = ExecutorCrawler(factory=_cf, mode=RunningMode.Concurrent, executors=3)
        return _sc


    def test_run(self, crawler: ExecutorCrawler):
        url = URL(base=Test_URL_TW_Stock_With_Option, start="20210801", end="20211001", formatter="yyyymmdd")
        url.set_period(days=31, hours=0, minutes=0, seconds=0)
        target_urls = url.generate()

        data = crawler.run(method="GET", url=target_urls, lock=False, sema_value=3)
        assert data is not None, f"It should get some data finally."



class TestPoolCrawler(BaseCrawlerTestSpec):

    @pytest.fixture
    def crawler(self) -> BaseCrawler:
        _cf = CrawlerFactory()
        _cf.http_factory = StockHTTPRequest(retry_components=MyRetry())
        _cf.parser_factory = StockHTTPResponseParser()
        _cf.data_handling_factory = StockDataHandler()

        _sc = PoolCrawler(factory=_cf, mode=RunningMode.Parallel, pool_size=5, tasks_size=3)
        return _sc


    def test_run(self, crawler: PoolCrawler):
        crawler.http_io = StockHTTPRequest(retry_components=MyRetry())
        crawler.http_response_parser = StockHTTPResponseParser()
        crawler.data_handler = StockDataHandler()

        crawler.init(lock=False, sema_value=3)
        data = crawler.async_apply(method="GET", url=Test_URL_TW_Stock)
        crawler.close()

        assert data is not None, f"It should get some data finally."


    def test_run_by_python_keyword_with(self, crawler: PoolCrawler):
        with crawler as _pc:
            _pc.http_io = StockHTTPRequest(retry_components=MyRetry())
            _pc.http_response_parser = StockHTTPResponseParser()
            _pc.data_handler = StockDataHandler()

            _pc.init(lock=False, sema_value=3)
            data = _pc.async_apply(method="GET", url=Test_URL_TW_Stock)
            assert data is not None, f"It should get some data finally."


