from smoothcrawler.components.data import BaseHTTPResponseParser, BaseDataHandler, BaseAsyncHTTPResponseParser, BaseAsyncDataHandler, T

from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
from typing import Union, Any, Generic
from urllib3 import PoolManager, HTTPResponse
from requests import Response
import asyncio
import aiohttp
import sys


Test_URL = "http://www.example.com/"

Handled_HTTP_200_Response_Flag = False
Handled_HTTP_Not_200_Response_Flag = False


def _init_flag():
    global Handled_HTTP_200_Response_Flag, Handled_HTTP_Not_200_Response_Flag
    Handled_HTTP_200_Response_Flag = False
    Handled_HTTP_Not_200_Response_Flag = False


def send_http_request(url: str) -> Union[Response, HTTPResponse]:
    _http = PoolManager()
    response = _http.request("GET", url)
    return response


async def async_send_http_request(url: str) -> aiohttp.client.ClientResponse:
    async with aiohttp.ClientSession() as _async_sess:
        _resp = await _async_sess.get(url)
        return _resp


class _MyHTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self, response) -> int:
        return int(response.status)


    def handling_200_response(self, response) -> Any:
        global Handled_HTTP_200_Response_Flag
        Handled_HTTP_200_Response_Flag = True
        return super(_MyHTTPResponseParser, self).handling_200_response(response)


    def handling_not_200_response(self, response) -> Any:
        global Handled_HTTP_Not_200_Response_Flag
        Handled_HTTP_Not_200_Response_Flag = True
        return super(_MyHTTPResponseParser, self).handling_not_200_response(response)



class _Not200HTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self, response) -> int:
        return 300


    def handling_200_response(self, response) -> Any:
        global Handled_HTTP_200_Response_Flag
        Handled_HTTP_200_Response_Flag = True
        return super(_Not200HTTPResponseParser, self).handling_200_response(response)


    def handling_not_200_response(self, response) -> Any:
        global Handled_HTTP_Not_200_Response_Flag
        Handled_HTTP_Not_200_Response_Flag = True
        return "Invalid Website"



class _Not200AsyncHTTPResponseParser(BaseAsyncHTTPResponseParser):

    async def get_status_code(self, response) -> int:
        return 300


    async def handling_200_response(self, response) -> Any:
        global Handled_HTTP_200_Response_Flag
        Handled_HTTP_200_Response_Flag = True
        return response


    async def handling_not_200_response(self, response) -> Any:
        global Handled_HTTP_Not_200_Response_Flag
        Handled_HTTP_Not_200_Response_Flag = True
        return "Invalid Website"


class _MyExampleHTTPResponseParser(BaseHTTPResponseParser):

    def get_status_code(self, response) -> int:
        return int(response.status)


    def handling_200_response(self, response: HTTPResponse) -> Any:
        global Handled_HTTP_200_Response_Flag
        Handled_HTTP_200_Response_Flag = True
        response_content = response.data.decode('utf-8')
        _bs = BeautifulSoup(response_content, "html.parser")
        _example_web_title = _bs.find_all("h1")
        return _example_web_title[0].text


    def handling_not_200_response(self, response) -> Any:
        global Handled_HTTP_Not_200_Response_Flag
        Handled_HTTP_Not_200_Response_Flag = True
        return super(_MyExampleHTTPResponseParser, self).handling_not_200_response(response)



class _MyExampleDataHandler(BaseDataHandler):

    def process(self, result) -> Generic[T]:
        return "Because I got " + result + ", I like to move it, move it."


class _MyExampleAsyncHTTPResponseParser(BaseAsyncHTTPResponseParser):

    async def get_status_code(self, response: aiohttp.client.ClientResponse) -> int:
        return int(response.status)


    async def handling_200_response(self, response: aiohttp.client.ClientResponse) -> Any:
        global Handled_HTTP_200_Response_Flag
        Handled_HTTP_200_Response_Flag = True
        _data = await response.text()
        response.release()
        _bs = BeautifulSoup(_data, "html.parser")
        _example_web_title = _bs.find_all("h1")
        return _example_web_title[0].text


    async def handling_not_200_response(self, response: aiohttp.client.ClientResponse) -> Any:
        global Handled_HTTP_Not_200_Response_Flag
        Handled_HTTP_Not_200_Response_Flag = True
        return response



class _MyExampleAsyncDataHandler(BaseAsyncDataHandler):

    async def process(self, result) -> Generic[T]:
        return "Because I got " + result + ", I like to move it, move it."



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



class BaseDataHandleTestSpec(metaclass=ABCMeta):

    @abstractmethod
    def test_process(self):
        pass



class TestHTTPResponseParser(BaseHTTPResponseParserTestSpec):

    def test_work_flow(self):
        _init_flag()

        response = send_http_request(url=Test_URL)
        parser = _MyHTTPResponseParser()
        status_code = parser.get_status_code(response=response)
        assert status_code == response.status, \
            "These 2 objects should be the same so that the attribute value also the same."

        handled_response = parser.parse_content(response=response)
        assert Handled_HTTP_200_Response_Flag is True, \
            "It should run the method 'handle_http_200_response' if you don't override it."
        assert Handled_HTTP_Not_200_Response_Flag is False, \
            "It should not run the method 'handle_http_not_200_response' if you don't override 'parse_content' and response is successful."

        assert response.data == handled_response.data, "For the default return value, it won't do anything for HTTP response object."


    def test_get_http_status_code(self):
        _init_flag()

        response = send_http_request(url=Test_URL)
        parser = _MyHTTPResponseParser()
        status_code = parser.get_status_code(response=response)
        assert status_code == 200, "It should be a HTTP response object with HTTP status code."
        assert status_code == response.status, \
            "These 2 objects should be the same so that the attribute value also the same."


    def test_handle_http_200_response(self):
        _init_flag()

        response = send_http_request(url=Test_URL)
        parser = _MyExampleHTTPResponseParser()
        parsed_result = parser.parse_content(response=response)
        assert Handled_HTTP_200_Response_Flag is True, \
            f"It should run the method 'handle_http_200_response' because {Test_URL} is activate."
        assert Handled_HTTP_Not_200_Response_Flag is False, \
            f"It should not run the method 'handle_http_not_200_response' because {Test_URL} is activate."
        assert parsed_result == "Example Domain", f"It should get the target website '{Test_URL}' content and parse the web title."


    def test_handle_http_not_200_response(self):
        _init_flag()

        response = send_http_request(url=Test_URL)
        parser = _Not200HTTPResponseParser()
        parsed_result = parser.parse_content(response=response)
        assert Handled_HTTP_200_Response_Flag is False, \
            "It should not run the method 'handle_http_200_response' because status_code always return 300 in class '_Not200HTTPResponseParser'."
        assert Handled_HTTP_Not_200_Response_Flag is True, \
            "It should run the method 'handle_http_not_200_response' because status_code always return 300 in class '_Not200HTTPResponseParser'."
        assert parsed_result == "Invalid Website", "It should return the value 'Invalid Website'."


def _run_async_func(_callable):
    if "3.6" in sys.version:
        _event_loop = asyncio.get_event_loop()
        _event_loop.run_until_complete(_callable())
    else:
        asyncio.run(_callable())


class TestAsyncHTTPResponseParser(BaseHTTPResponseParserTestSpec):

    def test_work_flow(self):
        _init_flag()

        async def _process():
            response = await async_send_http_request(url=Test_URL)
            parser = _MyExampleAsyncHTTPResponseParser()
            status_code = await parser.get_status_code(response=response)
            assert status_code == response.status, \
                "These 2 objects should be the same so that the attribute value also the same."

            handled_response = await parser.parse_content(response=response)
            assert Handled_HTTP_200_Response_Flag is True, \
                "It should run the method 'handle_http_200_response' if you don't override it."
            assert Handled_HTTP_Not_200_Response_Flag is False, \
                "It should not run the method 'handle_http_not_200_response' if you don't override 'parse_content' and response is successful."

            assert handled_response in await response.text(), "The parsed result data should be exist in original content data."

        _run_async_func(_process)


    def test_get_http_status_code(self):
        _init_flag()

        async def _process():
            response = await async_send_http_request(url=Test_URL)
            parser = _MyExampleAsyncHTTPResponseParser()
            status_code = await parser.get_status_code(response=response)
            assert status_code == 200, "It should be a HTTP response object with HTTP status code."
            assert status_code == response.status, \
                "These 2 objects should be the same so that the attribute value also the same."

        _run_async_func(_process)


    def test_handle_http_200_response(self):
        _init_flag()

        async def _process():
            response = await async_send_http_request(url=Test_URL)
            parser = _MyExampleAsyncHTTPResponseParser()
            parsed_result = await parser.parse_content(response=response)
            assert Handled_HTTP_200_Response_Flag is True, \
                f"It should run the method 'handle_http_200_response' because {Test_URL} is activate."
            assert Handled_HTTP_Not_200_Response_Flag is False, \
                f"It should not run the method 'handle_http_not_200_response' because {Test_URL} is activate."
            assert parsed_result == "Example Domain", f"It should get the target website '{Test_URL}' content and parse the web title."

        _run_async_func(_process)


    def test_handle_http_not_200_response(self):
        _init_flag()

        async def _process():
            response = await async_send_http_request(url=Test_URL)
            parser = _Not200AsyncHTTPResponseParser()
            parsed_result = await parser.parse_content(response=response)
            assert Handled_HTTP_200_Response_Flag is False, \
                "It should not run the method 'handle_http_200_response' because status_code always return 300 in class '_Not200HTTPResponseParser'."
            assert Handled_HTTP_Not_200_Response_Flag is True, \
                "It should run the method 'handle_http_not_200_response' because status_code always return 300 in class '_Not200HTTPResponseParser'."
            assert parsed_result == "Invalid Website", "It should return the value 'Invalid Website'."

        _run_async_func(_process)



class TestDataHandler(BaseDataHandleTestSpec):

    def test_process(self):
        _init_flag()

        response = send_http_request(url=Test_URL)
        parser = _MyExampleHTTPResponseParser()
        data_handler = _MyExampleDataHandler()
        parsed_result = parser.parse_content(response=response)
        handled_data = data_handler.process(result=parsed_result)
        assert handled_data == f"Because I got {parsed_result}, I like to move it, move it.", "The handled data format should conform to the implementation of data processing in class '_MyExampleDataHandler'."



class TestAsyncDataHandler(BaseDataHandleTestSpec):

    def test_process(self):
        _init_flag()

        async def _process():
            response = await async_send_http_request(url=Test_URL)
            parser = _MyExampleAsyncHTTPResponseParser()
            data_handler = _MyExampleAsyncDataHandler()
            parsed_result = await parser.parse_content(response=response)
            handled_data = await data_handler.process(result=parsed_result)
            assert handled_data == f"Because I got {parsed_result}, I like to move it, move it.", "The handled data format should conform to the implementation of data processing in class '_MyExampleDataHandler'."

        _run_async_func(_process)

