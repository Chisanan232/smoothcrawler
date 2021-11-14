# Import package multirunnable
import pathlib
import sys
import os

package_dir_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
multirunnable_path = os.path.join(package_dir_path, "apache-multirunnable")
sys.path.append(multirunnable_path)

package_dir_path_2 = str(pathlib.Path(__file__).absolute().parent.parent.parent)
smoothcrawler_path = os.path.join(package_dir_path_2, "apache-smoothcrawler")
sys.path.append(smoothcrawler_path)

print("multirunnable: ", multirunnable_path)


from smoothcrawler.crawler import SimpleCrawler, ExecutorCrawler, PoolCrawler
from smoothcrawler.httpio import set_retry
from smoothcrawler.urls import URL
from smoothcrawler import RunningMode

from crawler_components import MyRetry, StockHTTPRequest, StockHTTPResponseParser, StockDataHandler
from crawler_layer import StockDao, StockFao


HTTP_METHOD = "GET"
Test_URL_TW_Stock = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20210801&stockNo=2330"
Test_URL_TW_Stock_With_Option = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date={date}&stockNo=2330"


def run_as_simple_crawler():
    # Crawler Role: Simple Crawler
    sc = SimpleCrawler()
    sc.http_io = StockHTTPRequest(retry_components=MyRetry())
    sc.http_response_parser = StockHTTPResponseParser()
    sc.data_handler = StockDataHandler()
    data = sc.run("GET", Test_URL_TW_Stock)
    print(f"[DEBUG] data: {data}")



def run_as_executor_crawler():
    # Crawler Role: Executor Crawler
    sc = ExecutorCrawler(mode=RunningMode.Concurrent, executors=3)
    sc.http_io = StockHTTPRequest(retry_components=MyRetry())
    sc.http_response_parser = StockHTTPResponseParser()
    sc.data_handler = StockDataHandler()
    url = URL(base=Test_URL_TW_Stock_With_Option, start="20210801", end="20211001", formatter="yyyymmdd")
    url.set_period(days=31, hours=0, minutes=0, seconds=0)
    target_urls = url.generate()
    print(f"Target URLs: {target_urls}")
    data = sc.run(method="GET", url=target_urls, lock=False, sema_value=3)
    for d in data:
        print(f"[DEBUG] pid: {d.pid}")
        print(f"[DEBUG] worker_id: {d.worker_id}")
        print(f"[DEBUG] state: {d.state}")
        print(f"[DEBUG] exception: {d.exception}")
        print(f"[DEBUG] data: {d.data}")



def run_as_pool_crawler():
    # # Crawler Role: Pool Crawler
    with PoolCrawler(mode=RunningMode.Parallel, pool_size=5, tasks_size=3) as pc:
        pc.http_io = StockHTTPRequest(retry_components=MyRetry())
        pc.http_response_parser = StockHTTPResponseParser()
        pc.data_handler = StockDataHandler()

        pc.init(lock=False, sema_value=3)
        data = pc.async_apply(method="GET", url=Test_URL_TW_Stock)
        for d in data:
            print(f"[DEBUG] pid: {d.pid}")
            print(f"[DEBUG] worker_id: {d.worker_id}")
            print(f"[DEBUG] state: {d.state}")
            print(f"[DEBUG] exception: {d.exception}")
            print(f"[DEBUG] data: {d.data}")



if __name__ == '__main__':

    set_retry(3)
    print("Set retry times.")

    print("++++++++++++++ Simple Crawler ++++++++++++++++++")
    run_as_simple_crawler()

    print("++++++++++++++ Executor Crawler ++++++++++++++++++")
    run_as_executor_crawler()

    print("++++++++++++++ Pool Crawler ++++++++++++++++++")
    run_as_pool_crawler()

    print("All task done.")
