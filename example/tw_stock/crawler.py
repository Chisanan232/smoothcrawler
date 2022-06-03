from smoothcrawler.crawler import RunAsParallel, RunAsConcurrent, RunAsCoroutine, SimpleCrawler, AsyncSimpleCrawler, ExecutorCrawler, PoolCrawler
from smoothcrawler.factory import CrawlerFactory, AsyncCrawlerFactory
from smoothcrawler.urls import URL

from example.components.http_sender import Urllib3HTTPRequest, RequestsHTTPRequest, AsyncHTTPRequest
from example.components.persistence import StockDataPersistenceLayer
from .http_parser import Urllib3StockHTTPResponseParser, RequestsStockHTTPResponseParser, StockAsyncHTTPResponseParser
from .data_handler import StockDataHandler, StockAsyncDataHandler


HTTP_METHOD = "GET"
Test_URL_TW_Stock = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210101&stockNo=8454"
Test_URL_TW_Stock_With_Option = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo=2330"



class StockCrawlerImpl:

    def __init__(self):
        self._cf = CrawlerFactory()
        self._cf.http_factory = Urllib3HTTPRequest()
        self._cf.parser_factory = Urllib3StockHTTPResponseParser()
        self._cf.data_handling_factory = StockDataHandler()
        self._cf.persistence_factory = StockDataPersistenceLayer()

        self._acf = AsyncCrawlerFactory()
        self._acf.http_factory = AsyncHTTPRequest()
        self._acf.parser_factory = StockAsyncHTTPResponseParser()
        self._acf.data_handling_factory = StockAsyncDataHandler()
        self._cf.persistence_factory = StockDataPersistenceLayer()


    def run_as_simple_crawler(self):
        # _cf.persistence_factory = StockDataPersistenceLayer()

        # Crawler Role: Simple Crawler
        sc = SimpleCrawler(factory=self._cf)
        data = sc.run("GET", Test_URL_TW_Stock)
        print(f"[DEBUG] data: {data}")
        # sc.run_and_save("GET", Test_URL_TW_Stock)


    def run_as_async_simple_crawler(self):
        # Generate URLs
        url = URL(base=Test_URL_TW_Stock_With_Option, start="20210801", end="20211001", formatter="yyyymmdd")
        url.set_period(days=31, hours=0, minutes=0, seconds=0)
        target_urls = url.generate()
        print(f"Target URLs: {target_urls}")

        # Crawler Role: Asynchronous Simple Crawler
        sc = AsyncSimpleCrawler(factory=self._acf, executors=2)
        data = sc.run("GET", target_urls)
        print(f"[DEBUG] data: {data}")


    def run_as_executor_crawler(self):
        # Generate URLs
        url = URL(base=Test_URL_TW_Stock_With_Option, start="20210801", end="20211001", formatter="yyyymmdd")
        url.set_period(days=31, hours=0, minutes=0, seconds=0)
        target_urls = url.generate()
        print(f"Target URLs: {target_urls}")

        # Crawler Role: Executor Crawler
        sc = ExecutorCrawler(factory=self._cf, mode=RunAsParallel, executors=3)
        data = sc.run(method="GET", url=target_urls, lock=False, sema_value=3)
        print(f"[DEBUG] data: {data}")
        for d in data:
            print(f"[DEBUG] pid: {d.pid}")
            print(f"[DEBUG] worker_id: {d.worker_ident}")
            print(f"[DEBUG] state: {d.state}")
            print(f"[DEBUG] exception: {d.exception}")
            print(f"[DEBUG] data: {d.data}")


    def run_as_pool_crawler(self):
        # Generate URLs
        url = URL(base=Test_URL_TW_Stock_With_Option, start="20210801", end="20211001", formatter="yyyymmdd")
        url.set_period(days=31, hours=0, minutes=0, seconds=0)
        target_urls = url.generate()
        print(f"Target URLs: {target_urls}")

        # # Crawler Role: Pool Crawler
        with PoolCrawler(factory=self._cf, mode=RunAsParallel, pool_size=5) as pc:
            # pc.init(lock=False, sema_value=3)
            data = pc.async_apply(method="GET", urls=target_urls)
            print(f"[DEBUG] data: {data}")
            for d in data:
                print(f"[DEBUG] data: {d.data}")
                print(f"[DEBUG] is_successful: {d.is_successful}")


