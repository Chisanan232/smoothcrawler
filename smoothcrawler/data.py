from abc import ABCMeta, abstractmethod
from http import HTTPStatus
from typing import List, Dict, Union, Any
# from urllib3.response import HTTPResponse
# from requests import Response



class BaseHTTPResponseParser(metaclass=ABCMeta):

    _HTTPResponse = None

    def __init__(self, response):
        self._HTTPResponse = response


    def parse_content(self) -> Any:
        if self.get_status_code() == HTTPStatus.OK.real:
            handled_result = self.handling_200_response()
        else:
            handled_result = self.handling_not_200_response()
        return handled_result


    @abstractmethod
    def get_status_code(self) -> int:
        pass


    def handling_200_response(self) -> Any:
        return self._HTTPResponse


    def handling_not_200_response(self) -> Any:
        return self._HTTPResponse



class BaseDataHandler(metaclass=ABCMeta):

    @abstractmethod
    def process(self, result):
        pass


