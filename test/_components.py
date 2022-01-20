from smoothcrawler.components.data import BaseHTTPResponseParser, BaseDataHandler, BaseAsyncHTTPResponseParser, BaseAsyncDataHandler
from smoothcrawler.components.httpio import HTTP, RetryComponent, AsyncHTTP, AsyncRetryComponent
from smoothcrawler.persistence import PersistenceFacade
from smoothcrawler.persistence.file import SavingStrategy
from typing import Any
import requests
import urllib3
import aiohttp
import random
import json
import time

from ._persistence_layer import StockDao, StockFao


_database_config = {
    "host": "127.0.0.1",
    # "host": "172.17.0.6",
    "port": "3306",
    "user": "root",
    "password": "password",
    "database": "tw_stock"
}


class MyRetry(RetryComponent):

    def before_request(self, *args, **kwargs):
        print("Initial process.")

    def request_done(self, result):
        print("Task done! ")
        return result

    def request_final(self):
        print("Task done! ")

    def request_error(self, error):
        print("Got failure when run task.")
        return error



class Urllib3HTTPRequest(HTTP):

    __Http_Response = None

    def get(self, url: str, *args, **kwargs):
        _http = urllib3.PoolManager()
        _random_sleep = random.randrange(0, 10)
        time.sleep(_random_sleep)
        self.__Http_Response = _http.request("GET", url)
        return self.__Http_Response



class RequestsHTTPRequest(HTTP):

    __Http_Response = None

    def get(self, url: str, *args, **kwargs):
        _random_sleep = random.randrange(0, 10)
        time.sleep(_random_sleep)
        self.__Http_Response = requests.get(url)
        return self.__Http_Response



class StockAsyncHTTPRequest(AsyncHTTP):

    __Http_Response = None

    async def get(self, url: str, *args, **kwargs):
        async with aiohttp.ClientSession() as _async_sess:
            _resp = await _async_sess.get(url)
            return _resp



class Urllib3StockHTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self, response: urllib3.response.HTTPResponse) -> int:
        return response.status


    def handling_200_response(self, response: urllib3.response.HTTPResponse) -> Any:
        _data = response.data.decode('utf-8')
        return _data



class RequestsStockHTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self, response: requests.Response) -> int:
        return response.status_code


    def handling_200_response(self, response: requests.Response) -> Any:
        _data = response.json()
        return _data



class StockAsyncHTTPResponseParser(BaseAsyncHTTPResponseParser):

    async def get_status_code(self, response: aiohttp.client.ClientResponse) -> int:
        return response.status


    async def handling_200_response(self, response: aiohttp.client.ClientResponse) -> Any:
        _data = await response.json()
        response.release()
        return _data


    async def handling_not_200_response(self, response: aiohttp.client.ClientResponse) -> Any:
        return response



class StockDataHandler(BaseDataHandler):

    def process(self, result):
        _result_json = json.loads(result)
        _result_data = _result_json["data"]

        _final_data = []
        _data_row = []

        for _d in _result_data:
            # # stock_date
            _data_row.append(_d[0].replace("/", "-"))
            # # trade_volume
            _data_row.append(int(_d[1].replace(",", "")))
            # # turnover_price
            _data_row.append(int(_d[2].replace(",", "")))
            # # opening_price
            _data_row.append(float(_d[3]))
            # # highest_price
            _data_row.append(float(_d[4]))
            # # lowest_price
            _data_row.append(float(_d[5]))
            # # closing_price
            _data_row.append(float(_d[6]))
            # # gross_spread
            _data_row.append(str(_d[7]))
            # # turnover_volume
            _data_row.append(int(_d[8].replace(",", "")))

            _final_data.append(_data_row.copy())
            _data_row[:] = []

        return _final_data



class StockAsyncDataHandler(BaseAsyncDataHandler):

    async def process(self, result):
        _result_json = json.loads(result)
        _result_data = _result_json["data"]

        _final_data = []
        _data_row = []

        for _d in _result_data:
            # # stock_date
            _data_row.append(_d[0].replace("/", "-"))
            # # trade_volume
            _data_row.append(int(_d[1].replace(",", "")))
            # # turnover_price
            _data_row.append(int(_d[2].replace(",", "")))
            # # opening_price
            _data_row.append(float(_d[3]))
            # # highest_price
            _data_row.append(float(_d[4]))
            # # lowest_price
            _data_row.append(float(_d[5]))
            # # closing_price
            _data_row.append(float(_d[6]))
            # # gross_spread
            _data_row.append(str(_d[7]))
            # # turnover_volume
            _data_row.append(int(_d[8].replace(",", "")))

            _final_data.append(_data_row.copy())
            _data_row[:] = []

        return _final_data



class StockDataFilePersistenceLayer(PersistenceFacade):

    def save(self, data, *args, **kwargs):
        _stock_fao = StockFao(strategy=SavingStrategy.ONE_THREAD_ONE_FILE)
        _stock_fao.save(formatter="csv", file="/Users/bryantliu/Downloads/stock_crawler_2330.csv", mode="a+", data=data)



class StockDataDatabasePersistenceLayer(PersistenceFacade):

    def save(self, data, *args, **kwargs):
        _stock_dao = StockDao(**_database_config)
        _stock_dao.create_stock_data_table(stock_symbol="2330")
        _data_rows = [tuple(d) for d in data]
        _stock_dao.batch_insert(stock_symbol="2330", data=_data_rows)

