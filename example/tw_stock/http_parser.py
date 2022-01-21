from smoothcrawler.components.data import BaseHTTPResponseParser, BaseAsyncHTTPResponseParser
from typing import Any
import requests
import urllib3
import aiohttp



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

