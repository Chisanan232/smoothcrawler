from smoothcrawler.components.persistence import PersistenceFacade
from smoothcrawler.components.httpio import HTTP, AsyncHTTP
from smoothcrawler.components.data import BaseHTTPResponseParser, BaseDataHandler, BaseAsyncHTTPResponseParser, BaseAsyncDataHandler
from multirunnable.persistence.file import SavingStrategy
from typing import Any
from bs4 import BeautifulSoup
import requests
import urllib3
import aiohttp

from ._persistence_layer import StockDao, StockFao



class Urllib3HTTPRequest(HTTP):

    __Http_Response = None

    def get(self, url: str, *args, **kwargs):
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("GET", url)
        return self.__Http_Response



class RequestsHTTPRequest(HTTP):

    __Http_Response = None

    def get(self, url: str, *args, **kwargs):
        self.__Http_Response = requests.get(url)
        return self.__Http_Response



class AsyncHTTPRequest(AsyncHTTP):

    __Http_Response = None

    async def get(self, url: str, *args, **kwargs):
        async with aiohttp.ClientSession() as _async_sess:
            _resp = await _async_sess.get(url)
            return _resp



class Urllib3HTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self, response: urllib3.response.HTTPResponse) -> int:
        return response.status


    def handling_200_response(self, response: urllib3.response.HTTPResponse) -> Any:
        _bs = BeautifulSoup(response.read(), "html.parser")
        _example_web_title = _bs.find_all("h1")
        return _example_web_title



class RequestsHTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self, response: requests.Response) -> int:
        return response.status_code


    def handling_200_response(self, response: requests.Response) -> Any:
        _bs = BeautifulSoup(response.text, "html.parser")
        _example_web_title = _bs.find_all("h1")
        return _example_web_title



class AsyncHTTPResponseParser(BaseAsyncHTTPResponseParser):

    async def get_status_code(self, response: aiohttp.client.ClientResponse) -> int:
        return response.status


    async def handling_200_response(self, response: aiohttp.client.ClientResponse) -> Any:
        _html = await response.text()
        _bs = BeautifulSoup(_html, "html.parser")
        _example_web_title = _bs.find_all("h1")
        response.release()
        return _example_web_title


    async def handling_not_200_response(self, response: aiohttp.client.ClientResponse) -> Any:
        return response



class ExampleWebDataHandler(BaseDataHandler):

    def process(self, result):
        return result



class ExampleWebAsyncDataHandler(BaseAsyncDataHandler):

    async def process(self, result):
        return result



class DataFilePersistenceLayer(PersistenceFacade):

    def save(self, data, *args, **kwargs):
        _stock_fao = StockFao(strategy=SavingStrategy.ONE_THREAD_ONE_FILE)
        _stock_fao.save(formatter="csv", file="/Users/bryantliu/Downloads/stock_crawler_2330.csv", mode="a+", data=data)



class DataDatabasePersistenceLayer(PersistenceFacade):

    def save(self, data, *args, **kwargs):
        _stock_dao = StockDao()
        _stock_dao.create_stock_data_table(stock_symbol="2330")
        _data_rows = [tuple(d) for d in data]
        _stock_dao.batch_insert(stock_symbol="2330", data=_data_rows)

