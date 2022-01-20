from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic
import pytest

from smoothcrawler.crawler import (
    BaseCrawler,
    SimpleCrawler,
    AsyncSimpleCrawler,
    ExecutorCrawler,
    PoolCrawler,
    RunAsParallel, RunAsConcurrent, RunAsCoroutine)
from smoothcrawler.urls import URL
from smoothcrawler.factory import CrawlerFactory, AsyncCrawlerFactory

from ._components import (
    MyRetry,
    Urllib3HTTPRequest, RequestsHTTPRequest, AsyncHTTPRequest,
    Urllib3HTTPResponseParser, RequestsHTTPResponseParser, AsyncHTTPResponseParser,
    ExampleWebDataHandler, ExampleWebAsyncDataHandler,
    DataFilePersistenceLayer,
    DataDatabasePersistenceLayer)


T = TypeVar("T")

HTTP_METHOD = "GET"
Test_Example_URL = "http://www.example.com/"
Test_Example_URL_With_Option = "http://www.example.com?date={date}"


@pytest.fixture(scope="class")
def urls() -> list:
    _url = URL(base=Test_Example_URL_With_Option, start="20210801", end="20211201", formatter="yyyymmdd")
    _url.set_period(days=31, hours=0, minutes=0, seconds=0)
    _target_urls = _url.generate()
    return _target_urls


@pytest.fixture(scope="class")
def less_urls() -> list:
    _url = URL(base=Test_Example_URL_With_Option, start="20210801", end="20210901", formatter="yyyymmdd")
    _url.set_period(days=31, hours=0, minutes=0, seconds=0)
    _target_urls = _url.generate()
    return _target_urls


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



class TestSimpleCrawler(BaseCrawlerTestSpec):

    @pytest.fixture
    def crawler(self) -> BaseCrawler:
        _cf = CrawlerFactory()
        _cf.http_factory = Urllib3HTTPRequest(retry_components=MyRetry())
        _cf.parser_factory = Urllib3HTTPResponseParser()
        _cf.data_handling_factory = ExampleWebDataHandler()

        _sc = SimpleCrawler(factory=_cf)
        return _sc


    def test_run_with_one_url(self, crawler: SimpleCrawler):
        result = crawler.run("GET", Test_Example_URL)
        assert result is not None, f"It should get some data finally."


    def test_run_with_multiple_urls(self, crawler: SimpleCrawler, urls: list):
        result = crawler.run("GET", urls)
        assert result is not None, f"It should get some data finally."


    @pytest.mark.skip(reason="[TestSimpleCrawler.run_and_save] doesn't implement testing code.")
    def test_run_and_save(self, crawler: SimpleCrawler):
        result = crawler.run("GET", Test_Example_URL)
        assert result is not None, f"It should get some data finally."



class TestAsyncSimpleCrawler(BaseCrawlerTestSpec):

    @pytest.fixture
    def crawler(self) -> BaseCrawler:
        _acf = AsyncCrawlerFactory()
        _acf.http_factory = AsyncHTTPRequest()
        _acf.parser_factory = AsyncHTTPResponseParser()
        _acf.data_handling_factory = ExampleWebAsyncDataHandler()

        _sc = AsyncSimpleCrawler(factory=_acf, executors=3)
        return _sc


    def test_run_with_urls_list(self, crawler: AsyncSimpleCrawler, urls: list):
        result = crawler.run("GET", urls)
        assert result is not None, f"It should get some data finally."


    def test_run_with_urls_list_less_than_executors(self, crawler: AsyncSimpleCrawler, less_urls: list):
        result = crawler.run("GET", less_urls)
        assert result is not None, f"It should get some data finally."


    @pytest.mark.skip(reason="[TestAsyncSimpleCrawler.process_with_queue] doesn't implement testing code.")
    def test_run_with_urls_queue(self, crawler: AsyncSimpleCrawler, urls: list):
        result = crawler.run("GET", urls)
        assert result is not None, f"It should get some data finally."



class TestExecutorCrawler(BaseCrawlerTestSpec):

    @pytest.fixture
    def crawler(self) -> BaseCrawler:
        _cf = CrawlerFactory()
        _cf.http_factory = Urllib3HTTPRequest(retry_components=MyRetry())
        _cf.parser_factory = Urllib3HTTPResponseParser()
        _cf.data_handling_factory = ExampleWebDataHandler()

        _sc = ExecutorCrawler(factory=_cf, mode=RunAsCoroutine, executors=3)
        return _sc


    def test_run_with_urls_list(self, crawler: ExecutorCrawler, urls: list):
        data = crawler.run(method="GET", url=urls, lock=False, sema_value=3)
        assert data is not None, f"It should get some data finally."


    def test_run_with_urls_list_less_than_executors(self, crawler: ExecutorCrawler, less_urls: list):
        data = crawler.run(method="GET", url=less_urls, lock=False, sema_value=3)
        assert data is not None, f"It should get some data finally."


    @pytest.mark.skip(reason="[TestExecutorCrawler.process_with_queue] doesn't implement testing code.")
    def test_run_with_urls_queue(self, crawler: ExecutorCrawler, urls: list):
        data = crawler.run(method="GET", url=urls, lock=False, sema_value=3)
        assert data is not None, f"It should get some data finally."



class TestPoolCrawler(BaseCrawlerTestSpec):

    @pytest.fixture
    def crawler(self) -> BaseCrawler:
        _cf = CrawlerFactory()
        # _cf.http_factory = Urllib3HTTPRequest()
        # _cf.parser_factory = Urllib3StockHTTPResponseParser()
        _cf.http_factory = RequestsHTTPRequest()
        _cf.parser_factory = RequestsHTTPResponseParser()
        _cf.data_handling_factory = ExampleWebDataHandler()

        _sc = PoolCrawler(factory=_cf, mode=RunAsConcurrent, pool_size=5, tasks_size=3)
        return _sc


    def test_apply(self, crawler: PoolCrawler):
        crawler.init(lock=False, sema_value=3)
        data = crawler.apply(method="GET", url=Test_Example_URL)
        crawler.close()

        assert data is not None, f"It should get some data finally."


    def test_apply_by_python_keyword_with(self, crawler: PoolCrawler):
        with crawler as _pc:
            _pc.init(lock=False, sema_value=3)
            data = _pc.apply(method="GET", url=Test_Example_URL)
            assert data is not None, f"It should get some data finally."


    def test_async_apply(self, crawler: PoolCrawler):
        crawler.init(lock=False, sema_value=3)
        data = crawler.async_apply(method="GET", url=Test_Example_URL)
        crawler.close()

        assert data is not None, f"It should get some data finally."


    def test_async_apply_by_python_keyword_with(self, crawler: PoolCrawler):
        with crawler as _pc:
            _pc.init(lock=False, sema_value=3)
            data = _pc.async_apply(method="GET", url=Test_Example_URL)
            assert data is not None, f"It should get some data finally."


    def test_map(self, crawler: PoolCrawler, urls: list):
        crawler.init(lock=False, sema_value=3)
        data = crawler.map(method="GET", urls=urls)
        crawler.close()

        assert data is not None, f"It should get some data finally."


    def test_map_by_python_keyword_with(self, crawler: PoolCrawler, urls: list):
        with crawler as _pc:
            _pc.init(lock=False, sema_value=3)
            data = _pc.map(method="GET", urls=urls)
            assert data is not None, f"It should get some data finally."


    def test_async_map(self, crawler: PoolCrawler, urls: list):
        crawler.init(lock=False, sema_value=3)
        data = crawler.async_map(method="GET", urls=urls)
        crawler.close()

        assert data is not None, f"It should get some data finally."


    def test_async_map_by_python_keyword_with(self, crawler: PoolCrawler, urls: list):
        with crawler as _pc:
            _pc.init(lock=False, sema_value=3)
            data = _pc.async_map(method="GET", urls=urls)
            assert data is not None, f"It should get some data finally."


