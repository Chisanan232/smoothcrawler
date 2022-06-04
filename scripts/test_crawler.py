from bs4 import BeautifulSoup
from typing import Any
from smoothcrawler.crawler import SimpleCrawler
from smoothcrawler.factory import CrawlerFactory
from smoothcrawler.components.data import BaseHTTPResponseParser, BaseDataHandler
from smoothcrawler.components.httpio import HTTP
import requests


Test_Example_URL = "http://www.example.com/"


class RequestsHTTPRequest(HTTP):

    __Http_Response = None

    def get(self, url: str, *args, **kwargs):
        self.__Http_Response = requests.get(url)
        return self.__Http_Response



class RequestsExampleHTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self, response: requests.Response) -> int:
        return response.status_code


    def handling_200_response(self, response: requests.Response) -> Any:
        _bs = BeautifulSoup(response.text, "html.parser")
        _example_web_title = _bs.find_all("h1")
        return _example_web_title[0].text



class ExampleDataHandler(BaseDataHandler):

    def process(self, result):
        return result



class ExampleWebCrawlerImpl:

    def __init__(self):
        self._cf = CrawlerFactory()
        self._cf.http_factory = RequestsHTTPRequest()
        self._cf.parser_factory = RequestsExampleHTTPResponseParser()
        self._cf.data_handling_factory = ExampleDataHandler()


    def run_as_simple_crawler(self):
        # Crawler Role: Simple Crawler
        sc = SimpleCrawler(factory=self._cf)
        data = sc.run("GET", Test_Example_URL)
        print(f"[DEBUG] data: {data}")



if __name__ == '__main__':

    _example_web_crawler = ExampleWebCrawlerImpl()
    _example_web_crawler.run_as_simple_crawler()

