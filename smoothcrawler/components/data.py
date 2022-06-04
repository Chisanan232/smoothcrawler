from typing import TypeVar, Generic
from http import HTTPStatus
from abc import ABCMeta, abstractmethod


T = TypeVar("T")


class BaseHTTPResponseParser(metaclass=ABCMeta):

    def parse_content(self, response) -> Generic[T]:
        """
        Parse the HTTP response object.

        :param response: The HTTP response object.
        :return: The data which has been parsed or handled from HTTP response.
        """

        if self.get_status_code(response=response) == HTTPStatus.OK.real:
            handled_result = self.handling_200_response(response=response)
        else:
            handled_result = self.handling_not_200_response(response=response)
        # Require the return value type is List, Dict or JSON, etc.
        return handled_result


    @abstractmethod
    def get_status_code(self, response) -> int:
        """
        Get the HTTP status code from the HTTP response.

        :param response:
        :return:
        """

        pass


    def handling_200_response(self, response) -> Generic[T]:
        """
        Handle the HTTP response object if it's HTTP status code is 200.

        :param response:
        :return:
        """

        return response


    def handling_not_200_response(self, response) -> Generic[T]:
        """
        Handle the HTTP response object if it's HTTP status code isn't 200.

        :param response:
        :return:
        """

        return response



class BaseAsyncHTTPResponseParser(BaseHTTPResponseParser):

    async def parse_content(self, response) -> Generic[T]:
        """
        The asynchronous version of *BaseHTTPResponseParser.parse_content*.

        :param response:
        :return:
        """

        _http_resp_status = await self.get_status_code(response=response)
        if _http_resp_status == HTTPStatus.OK.real:
            handled_result = await self.handling_200_response(response=response)
        else:
            handled_result = await self.handling_not_200_response(response=response)
        # Require the return value type is List, Dict or JSON, etc.
        return handled_result


    @abstractmethod
    async def get_status_code(self, response) -> int:
        """
        The asynchronous version of *BaseHTTPResponseParser.get_status_code*.

        :param response:
        :return:
        """

        pass


    async def handling_200_response(self, response) -> Generic[T]:
        """
        The asynchronous version of *BaseHTTPResponseParser.handling_200_response*.

        :param response:
        :return:
        """

        return response


    async def handling_not_200_response(self, response) -> Generic[T]:
        """
        The asynchronous version of *BaseHTTPResponseParser.handling_not_200_response*.

        :param response:
        :return:
        """

        return response



class BaseDataHandler(metaclass=ABCMeta):

    @abstractmethod
    def process(self, result) -> Generic[T]:
        """
        The implementation of data process.

        :param result:
        :return:
        """

        pass



class BaseAsyncDataHandler(metaclass=ABCMeta):

    @abstractmethod
    async def process(self, result) -> Generic[T]:
        """
        The asynchronous version of *BaseDataHandler.process*.

        :param result:
        :return:
        """

        pass


