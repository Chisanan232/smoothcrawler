from abc import ABCMeta, abstractmethod
from http import HTTPStatus
from typing import List, Dict, TypeVar, Generic, Union, Any


T = TypeVar("T")


class BaseHTTPResponseParser(metaclass=ABCMeta):

    def parse_content(self, response) -> Generic[T]:
        if self.get_status_code(response=response) == HTTPStatus.OK.real:
            handled_result = self.handling_200_response(response=response)
        else:
            handled_result = self.handling_not_200_response(response=response)
        # Require the return value type is List, Dict or JSON, etc.
        return handled_result


    @abstractmethod
    def get_status_code(self, response) -> int:
        pass


    def handling_200_response(self, response) -> Generic[T]:
        return response


    def handling_not_200_response(self, response) -> Generic[T]:
        return response


class BaseAsyncHTTPResponseParser(BaseHTTPResponseParser):

    async def parse_content(self, response) -> Generic[T]:
        _http_resp_status = await self.get_status_code(response=response)
        if _http_resp_status == HTTPStatus.OK.real:
            handled_result = await self.handling_200_response(response=response)
        else:
            handled_result = await self.handling_not_200_response(response=response)
        # Require the return value type is List, Dict or JSON, etc.
        return handled_result


    @abstractmethod
    async def get_status_code(self, response) -> int:
        pass


    async def handling_200_response(self, response) -> Generic[T]:
        return response


    async def handling_not_200_response(self, response) -> Generic[T]:
        return response



class BaseDataHandler(metaclass=ABCMeta):

    @abstractmethod
    def process(self, result) -> Generic[T]:
        pass



class BaseAsyncDataHandler(metaclass=ABCMeta):

    @abstractmethod
    async def process(self, result) -> Generic[T]:
        pass


