from smoothcrawler.components.data import BaseHTTPResponseParser, BaseAsyncHTTPResponseParser
from typing import Any
from bs4 import BeautifulSoup
import requests
import aiohttp



class RequestsExampleHTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self, response: requests.Response) -> int:
        return response.status_code


    def handling_200_response(self, response: requests.Response) -> Any:
        _bs = BeautifulSoup(response.text, "html.parser")
        _example_web_title = _bs.find_all("h1")
        return _example_web_title[0].text



class ExampleAsyncHTTPResponseParser(BaseAsyncHTTPResponseParser):

    async def get_status_code(self, response: aiohttp.client.ClientResponse) -> int:
        return response.status


    async def handling_200_response(self, response: aiohttp.client.ClientResponse) -> Any:
        _data = await response.text()
        response.release()
        _bs = BeautifulSoup(_data, "html.parser")
        _example_web_title = _bs.find_all("h1")
        return _example_web_title[0].text


    async def handling_not_200_response(self, response: aiohttp.client.ClientResponse) -> Any:
        return response

