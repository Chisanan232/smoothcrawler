from abc import ABCMeta, abstractmethod
from http import HTTPStatus
from typing import List, Dict, Union, Any



class BaseHTTPResponseParser(metaclass=ABCMeta):

    def parse_content(self, response) -> Any:
        if self.get_status_code(response=response) == HTTPStatus.OK.real:
            handled_result = self.handling_200_response(response=response)
        else:
            handled_result = self.handling_not_200_response(response=response)
        # Require the return value type is List, Dict or JSON, etc.
        return handled_result


    @abstractmethod
    def get_status_code(self, response) -> int:
        pass


    def handling_200_response(self, response) -> Any:
        return response


    def handling_not_200_response(self, response) -> Any:
        return response



class BaseDataHandler(metaclass=ABCMeta):

    @abstractmethod
    def process(self, result) -> Any:
        pass


