from abc import ABCMeta, abstractmethod
from typing import Union, Any
from urllib3.response import HTTPResponse
from requests import Response



class BaseHTTPResponseParser(metaclass=ABCMeta):

    HTTP_Status_Code_OK = 200
    _HTTPResponse: Union[HTTPResponse, Response] = None

    def __init__(self, response: Union[HTTPResponse, Response]):
        self._HTTPResponse = response


    def parse_content(self) -> Any:
        if self.get_status_code() == self.HTTP_Status_Code_OK:
            handled_result = self.handle_http_200_response()
        else:
            handled_result = self.handle_http_not_200_response()
        return handled_result


    @abstractmethod
    def get_status_code(self) -> int:
        pass


    def handle_http_200_response(self) -> Any:
        return self._HTTPResponse


    def handle_http_not_200_response(self) -> Any:
        return self._HTTPResponse



class BaseDataHandler(metaclass=ABCMeta):

    @abstractmethod
    def process(self, result):
        pass


