# Import package smoothcrawler
import pathlib
import sys
import os

_package_dir_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
_smoothcrawler_path = os.path.join(_package_dir_path, "apache-smoothcrawler")
sys.path.append(_smoothcrawler_path)

from tw_stock.easy_crawlers import TaiwanStockEasyCrawler
from example_web.easy_crawler import ExampleEasyCrawler


Test_Example_URL = "http://www.example.com/"
Test_URL_TW_Stock = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20210801&stockNo=2330"

# Target: Web
_example_easy_crawler = ExampleEasyCrawler()
_example_result = _example_easy_crawler.run("get", Test_Example_URL)
print(f"Example web crawler result: {_example_result}")


# Target: API
# _tw_stock_easy_crawler = TaiwanStockEasyCrawler()
# _tw_stock_result = _tw_stock_easy_crawler.run("get", Test_URL_TW_Stock)
# print(f"Taiwan stock market data: {_tw_stock_result}")

