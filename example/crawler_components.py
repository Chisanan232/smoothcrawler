from smoothcrawler.data import BaseHTTPResponseParser, BaseDataHandler
from smoothcrawler.httpio import HTTP, RetryComponent
from typing import Any
import urllib3



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



class StockHTTPRequest(HTTP):

    __Http_Response = None

    def get(self, url: str, *args, **kwargs):
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("GET", url)
        return self.__Http_Response



class StockHTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self, response: urllib3.response.HTTPResponse) -> int:
        return response.status


    def handling_200_response(self, response: urllib3.response.HTTPResponse) -> Any:
        _data = response.data.decode('utf-8')
        return _data



class StockDataHandler(BaseDataHandler):

    def process(self, result):
        print("Final data: ", result)
        return result


