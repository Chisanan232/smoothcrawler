# Import package smoothcrawler
import pathlib
import sys
import os

_package_dir_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
_smoothcrawler_path = os.path.join(_package_dir_path, "apache-smoothcrawler")
sys.path.append(_smoothcrawler_path)

from tw_stock.crawler import StockCrawlerImpl
from example_web.crawler import ExampleWebCrawlerImpl


# Target: Web
_example_crawler_impl = ExampleWebCrawlerImpl()
_example_crawler_impl.run_as_simple_crawler()


# Target: API
_stock_crawler_impl = StockCrawlerImpl()
_stock_crawler_impl.run_as_simple_crawler()
_stock_crawler_impl.run_as_async_simple_crawler()
_stock_crawler_impl.run_as_executor_crawler()
_stock_crawler_impl.run_as_pool_crawler()

