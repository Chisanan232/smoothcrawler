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


from smoothcrawler.crawler import RunAsParallel, RunAsConcurrent, RunAsCoroutine, SimpleCrawler, ExecutorCrawler, PoolCrawler
from smoothcrawler.factory import CrawlerFactory
from smoothcrawler.components.httpio import set_retry
from smoothcrawler.urls import URL
from smoothcrawler.persistence.file import SavingStrategy

from crawler_components import MyRetry, StockHTTPRequest, StockHTTPResponseParser, StockDataHandler, StockDataPersistenceLayer
from crawler_layer import StockDao, StockFao


HTTP_METHOD = "GET"
Test_URL_TW_Stock = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210801&stockNo=2330"
Test_URL_TW_Stock_With_Option = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date={date}&stockNo=2330"

_database_config = {
    "host": "127.0.0.1",
    # "host": "172.17.0.6",
    "port": "3306",
    "user": "root",
    "password": "password",
    "database": "tw_stock"
}

_Stock_Fao = StockFao(strategy=SavingStrategy.ONE_THREAD_ONE_FILE)
_Stock_Dao = StockDao(**_database_config)


_cf = CrawlerFactory()
_cf.http_factory = StockHTTPRequest(retry_components=MyRetry())
_cf.parser_factory = StockHTTPResponseParser()
_cf.data_handling_factory = StockDataHandler()


def run_as_simple_crawler():
    _cf.persistence_factory = StockDataPersistenceLayer()

    # Crawler Role: Simple Crawler
    sc = SimpleCrawler(factory=_cf)

    # data = sc.run("GET", Test_URL_TW_Stock)
    # print(f"[DEBUG] data: {data}")

    sc.run_and_save("GET", Test_URL_TW_Stock)
    # _Stock_Fao.save(formatter="csv", file="/Users/bryantliu/Downloads/stock_crawler_2330.csv", mode="a+", data=data)



def run_as_executor_crawler():
    # Crawler Role: Executor Crawler
    sc = ExecutorCrawler(factory=_cf, mode=RunAsParallel, executors=3)

    url = URL(base=Test_URL_TW_Stock_With_Option, start="20210801", end="20211001", formatter="yyyymmdd")
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



def run_as_pool_crawler():
    # # Crawler Role: Pool Crawler
    with PoolCrawler(factory=_cf, mode=RunAsParallel, pool_size=5, tasks_size=3) as pc:
        pc.init(lock=False, sema_value=3)
        data = pc.async_apply(method="GET", url=Test_URL_TW_Stock)
        print(f"[DEBUG] data: {data}")
        for d in data:
            print(f"[DEBUG] data: {d.data}")
            print(f"[DEBUG] is_successful: {d.is_successful}")



if __name__ == '__main__':

    set_retry(3)
    print("Set retry times.")

    print("++++++++++++++ Simple Crawler ++++++++++++++++++")
    run_as_simple_crawler()

    # print("++++++++++++++ Executor Crawler ++++++++++++++++++")
    # run_as_executor_crawler()

    # print("++++++++++++++ Pool Crawler ++++++++++++++++++")
    # run_as_pool_crawler()

    print("All task done.")
