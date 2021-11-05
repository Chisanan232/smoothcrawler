from smoothcrawler.data import BaseHTTPResponseParser, BaseDataHandler

from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod
from typing import Union, Any
from urllib3 import PoolManager, HTTPResponse
from requests import Response


Test_URL = "https://www.google.com"

Handled_HTTP_200_Response_Flag = False
Handled_HTTP_Not_200_Response_Flag = False


def send_http_request(url: str) -> Union[Response, HTTPResponse]:
    _http = PoolManager()
    response = _http.request("GET", url)
    return response


class _MyHTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self) -> int:
        return int(self._HTTPResponse.status)


    def handle_http_200_response(self) -> Any:
        global Handled_HTTP_200_Response_Flag
        Handled_HTTP_200_Response_Flag = True
        return super(_MyHTTPResponseParser, self).handle_http_200_response()


    def handle_http_not_200_response(self) -> Any:
        global Handled_HTTP_Not_200_Response_Flag
        Handled_HTTP_Not_200_Response_Flag = True
        return super(_MyHTTPResponseParser, self).handle_http_not_200_response()



class _Not200HTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self) -> int:
        return 300


    def handle_http_200_response(self) -> Any:
        global Handled_HTTP_200_Response_Flag
        Handled_HTTP_200_Response_Flag = True
        return super(_Not200HTTPResponseParser, self).handle_http_200_response()


    def handle_http_not_200_response(self) -> Any:
        global Handled_HTTP_Not_200_Response_Flag
        Handled_HTTP_Not_200_Response_Flag = True
        return super(_Not200HTTPResponseParser, self).handle_http_not_200_response()



class BaseHTTPResponseParserTestSpec(metaclass=ABCMeta):

    @abstractmethod
    def test_get_http_status_code(self):
        pass


    @abstractmethod
    def test_handle_http_200_response(self):
        pass


    @abstractmethod
    def test_handle_http_not_200_response(self):
        pass


    @abstractmethod
    def test_parse_response(self):
        pass



class BaseDataHandleTestSpec(metaclass=ABCMeta):

    @abstractmethod
    def test_process(self):
        pass



class TestHTTPResponseParser(BaseHTTPResponseParserTestSpec):

    def test_work_flow(self):
        TestHTTPResponseParser._init_flag()

        response = send_http_request(url=Test_URL)
        parser = _MyHTTPResponseParser(response=response)
        status_code = parser.get_status_code()
        assert status_code == response.status, \
            "These 2 objects should be the same so that the attribute value also the same."

        handled_response = parser.parse_content()
        assert Handled_HTTP_200_Response_Flag == True, \
            "It should run the method 'handle_http_200_response' if you don't override it."
        assert Handled_HTTP_Not_200_Response_Flag == False, \
            "It should not run the method 'handle_http_not_200_response' if you don't override 'parse_content' and response is successful."

        assert response.data == handled_response.data, "For the default return value, it won't do anything for HTTP response object."


    def test_get_http_status_code(self):
        response = send_http_request(url=Test_URL)
        parser = _MyHTTPResponseParser(response=response)
        status_code = parser.get_status_code()
        assert status_code == 200, "It should be a HTTP response object with HTTP status code."
        assert status_code == response.status, \
            "These 2 objects should be the same so that the attribute value also the same."


    def test_handle_http_200_response(self):
        pass


    def test_handle_http_not_200_response(self):
        pass


    def test_parse_response(self):
        pass


    @staticmethod
    def _init_flag():
        global Handled_HTTP_200_Response_Flag, Handled_HTTP_Not_200_Response_Flag
        Handled_HTTP_200_Response_Flag = False
        Handled_HTTP_Not_200_Response_Flag = False



class TestDataHandler(BaseDataHandleTestSpec):

    def test_process(self):
        pass
