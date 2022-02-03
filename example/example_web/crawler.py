from smoothcrawler.crawler import RunAsParallel, RunAsConcurrent, RunAsCoroutine, SimpleCrawler, AsyncSimpleCrawler, ExecutorCrawler, PoolCrawler
from smoothcrawler.factory import CrawlerFactory, AsyncCrawlerFactory
from smoothcrawler.urls import URL

from example.components.http_sender import Urllib3HTTPRequest, RequestsHTTPRequest, AsyncHTTPRequest
from .http_parser import RequestsExampleHTTPResponseParser, ExampleAsyncHTTPResponseParser
from .data_handler import ExampleDataHandler, ExampleAsyncDataHandler


HTTP_METHOD = "GET"
Test_Example_URL = "http://www.example.com/"
Test_Example_URL_With_Option = "http://www.example.com?date={date}"



class ExampleWebCrawlerImpl:

    def __init__(self):
        self._cf = CrawlerFactory()
        # self._cf.http_factory = Urllib3HTTPRequest(retry_components=MyRetry())
        self._cf.http_factory = RequestsHTTPRequest()
        self._cf.parser_factory = RequestsExampleHTTPResponseParser()
        self._cf.data_handling_factory = ExampleDataHandler()

        self._acf = AsyncCrawlerFactory()
        self._acf.http_factory = AsyncHTTPRequest()
        self._acf.parser_factory = ExampleAsyncHTTPResponseParser()
        self._acf.data_handling_factory = ExampleAsyncDataHandler()


    def run_as_simple_crawler(self):
        # Crawler Role: Simple Crawler
        sc = SimpleCrawler(factory=self._cf)

        data = sc.run("GET", Test_Example_URL)
        print(f"[DEBUG] data: {data}")


    def run_as_async_simple_crawler(self):
        # Crawler Role: Asynchronous Simple Crawler
        sc = AsyncSimpleCrawler(factory=self._acf, executors=2)

        url = URL(base=Test_Example_URL_With_Option, start="20210801", end="20211001", formatter="yyyymmdd")
        url.set_period(days=31, hours=0, minutes=0, seconds=0)
        target_urls = url.generate()
        print(f"Target URLs: {target_urls}")

        data = sc.run("GET", target_urls)
        print(f"[DEBUG] data: {data}")


    def run_as_executor_crawler(self):
        # Crawler Role: Executor Crawler
        sc = ExecutorCrawler(factory=self._cf, mode=RunAsParallel, executors=3)

        url = URL(base=Test_Example_URL_With_Option, start="20210801", end="20211001", formatter="yyyymmdd")
        url.set_period(days=31, hours=0, minutes=0, seconds=0)
        target_urls = url.generate()
        print(f"Target URLs: {target_urls}")

        data = sc.run(method="GET", url=target_urls, lock=False, sema_value=3)
        print(f"[DEBUG] data: {data}")
        for d in data:
            print(f"[DEBUG] pid: {d.pid}")
            print(f"[DEBUG] worker_id: {d.worker_ident}")
            print(f"[DEBUG] state: {d.state}")
            print(f"[DEBUG] exception: {d.exception}")
            print(f"[DEBUG] data: {d.data}")


    def run_as_pool_crawler(self):
        # # Crawler Role: Pool Crawler
        with PoolCrawler(factory=self._cf, mode=RunAsParallel, pool_size=5) as pc:
            pc.init(lock=False, sema_value=3)
            data = pc.async_apply(method="GET", urls=[Test_Example_URL_With_Option])
            print(f"[DEBUG] data: {data}")
            for d in data:
                print(f"[DEBUG] data: {d.data}")
                print(f"[DEBUG] is_successful: {d.is_successful}")

