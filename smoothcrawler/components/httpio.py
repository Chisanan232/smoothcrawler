from multirunnable.api import retry as _retry, async_retry as _async_retry
from typing import Callable, Any, Union, TypeVar, Generic
from enum import Enum
from abc import ABCMeta, abstractmethod
import re


HTTPResponse = TypeVar("HTTPResponse")


class HTTPMethod(Enum):

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTION = "OPTION"
    HEAD = "HEAD"


class BaseHTTP(metaclass=ABCMeta):

    def __init__(self):
        pass


    @abstractmethod
    def request(self, url: str, method: Union[str, HTTPMethod] = "GET", timeout: int = -1, *args, **kwargs) -> Generic[HTTPResponse]:
        """
        Send HTTP request. About retry mechanism, it could let you override the functions *before_request*,
        *request_done*, *request_final*, *request_fail* to customize implementations if it needs.

        * *before_request*
        Run before send HTTP request.

        * *request_done*
        Run after send HTTP request and it gets the HTTP response successfully without any exceptions.

        * *request_final*
        No matter it sends HTTP request successfully or not, it would run after send HTTP request finally.

        * *request_fail*
        Run if it gets any exceptions when it sends HTTP request.

        :param url: URL.
        :param method: HTTP method.
        :param timeout: How many it would retry to send HTTP request if it gets fail when sends request.
        :return: A HTTP response object.
        """

        pass


    @abstractmethod
    def get(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        """
        Send HTTP request by **GET** HTTP method.

        :param url: URL.
        :return: A HTTP response object.
        """

        pass


    @abstractmethod
    def post(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        """
        Send HTTP request by **POST** HTTP method.

        :param url: URL.
        :return: A HTTP response object.
        """

        pass


    @abstractmethod
    def put(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        """
        Send HTTP request by **PUT** HTTP method.

        :param url: URL.
        :return: A HTTP response object.
        """

        pass


    @abstractmethod
    def delete(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        """
        Send HTTP request by **DELETE** HTTP method.

        :param url: URL.
        :return: A HTTP response object.
        """

        pass


    @abstractmethod
    def head(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        """
        Send HTTP request by **HEAD** HTTP method.

        :param url: URL.
        :return: A HTTP response object.
        """

        pass


    @abstractmethod
    def option(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        """
        Send HTTP request by **OPTION** HTTP method.

        :param url: URL.
        :return: A HTTP response object.
        """

        pass


    @abstractmethod
    def status_code(self):
        """
        Send HTTP request by **GET** HTTP method.

        :return:
        """

        pass



class HTTP(BaseHTTP):

    def __init__(self):
        super().__init__()


    def request(self, url: str, method: Union[str, HTTPMethod] = "GET", timeout: int = 1, *args, **kwargs) -> Generic[HTTPResponse]:

        _self = self

        @_retry.function(timeout=timeout)
        def __retry_request_process(_method: Union[str, HTTPMethod] = "GET", _timeout: int = 1, *_args, **_kwargs) -> Generic[HTTPResponse]:
            _response = self.__request_process(url=url, method=_method, timeout=_timeout, *_args, **_kwargs)
            return _response

        @__retry_request_process.initialization
        def _before_request(*_args, **_kwargs) -> None:
            self.__before(*_args, **_kwargs)

        @__retry_request_process.done_handling
        def _request_done(result):
            __result = self.__done(result)
            return __result

        @__retry_request_process.final_handling
        def _request_final() -> None:
            self.__final()

        @__retry_request_process.error_handling
        def _request_error(error: Exception):
            __error_handle = self.__error(error)
            return __error_handle

        response = __retry_request_process(method, timeout, *args, **kwargs)
        if response is TypeError and str(response) == f"Invalid HTTP method it got: '{method}'.":
            raise response
        return response


    def __request_process(self,
                          url: str,
                          method: Union[str, HTTPMethod] = "GET",
                          timeout: int = 1,
                          *args, **kwargs) -> Any:
        if re.search(r"get", method, re.IGNORECASE) or method is HTTPMethod.GET:
            response = self.get(url, *args, **kwargs)
        elif re.search(r"post", method, re.IGNORECASE) or method is HTTPMethod.POST:
            response = self.post(url, *args, **kwargs)
        elif re.search(r"put", method, re.IGNORECASE) or method is HTTPMethod.PUT:
            response = self.put(url, *args, **kwargs)
        elif re.search(r"delete", method, re.IGNORECASE) or method is HTTPMethod.DELETE:
            response = self.delete(url, *args, **kwargs)
        elif re.search(r"head", method, re.IGNORECASE) or method is HTTPMethod.HEAD:
            response = self.head(url, *args, **kwargs)
        elif re.search(r"option", method, re.IGNORECASE) or method is HTTPMethod.OPTION:
            response = self.option(url, *args, **kwargs)
        else:
            response = TypeError(f"Invalid HTTP method it got: '{method.upper()}'.")
        return response


    def get(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        return None


    def post(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        return None


    def put(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        return None


    def delete(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        return None


    def head(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        return None


    def option(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        return None


    @property
    def __before(self) -> Callable:
        return self.before_request


    @property
    def __done(self) -> Callable:
        return self.request_done


    @property
    def __final(self) -> Callable:
        return self.request_final


    @property
    def __error(self) -> Callable:
        return self.request_fail


    def before_request(self, *args, **kwargs) -> None:
        """
        This function would be called before it sends HTTP request.

        :return: None
        """

        pass


    def request_done(self, result) -> Any:
        """
        This function would be called after it sends HTTP request and it runs finely without any exceptions.

        :param result: The result of sending HTTP request. In generally, it's HTTP response object.
        :return: The handled result.
        """

        return result


    def request_fail(self, error: Exception) -> None:
        """
        This function would be called if it gets fail when it sends HTTP request.

        :param error: The exception it get.
        :return: None
        """

        raise error


    def request_final(self) -> None:
        """
        No matter it sends HTTP request successfully or not, this function must be called fianlly.

        :return: None
        """

        pass


    def status_code(self):
        pass



class AsyncHTTP(BaseHTTP):

    def __init__(self):
        super().__init__()


    async def request(self,
                      url: str,
                      method: Union[str, HTTPMethod] = "GET",
                      timeout: int = 1,
                      *args, **kwargs) -> Generic[HTTPResponse]:

        _self = self

        @_async_retry.function(timeout=timeout)
        async def __async_retry_request_process(_self, _method: Union[str, HTTPMethod] = "GET", _timeout: int = 1, *_args, **_kwargs) -> Generic[HTTPResponse]:
            __response = await _self.__request_process(url=url, method=_method, timeout=_timeout, *_args, **_kwargs)
            return __response

        @__async_retry_request_process.initialization
        async def _before_request(_self, *_args, **_kwargs):
            await self.__before_request(*_args, **_kwargs)

        @__async_retry_request_process.done_handling
        async def _request_done(_self, result):
            __result = await self.__request_done(result)
            return __result

        @__async_retry_request_process.final_handling
        async def _request_final(_self):
            await self.__request_final()

        @__async_retry_request_process.error_handling
        async def _request_error(_self, error):
            __error_handle = await self.__request_error(error)
            return __error_handle

        response = await __async_retry_request_process(self, method, timeout, *args, **kwargs)
        if response is TypeError and str(response) == f"Invalid HTTP method it got: '{method}'.":
            raise response
        return response


    async def __request_process(self,
                                url: str,
                                method: Union[str, HTTPMethod] = "GET",
                                timeout: int = 1,
                                *args, **kwargs) -> Generic[HTTPResponse]:
        if re.search(r"get", method, re.IGNORECASE) or method is HTTPMethod.GET:
            response = await self.get(url, *args, **kwargs)
        elif re.search(r"post", method, re.IGNORECASE) or method is HTTPMethod.POST:
            response = await self.post(url, *args, **kwargs)
        elif re.search(r"put", method, re.IGNORECASE) or method is HTTPMethod.PUT:
            response = await self.put(url, *args, **kwargs)
        elif re.search(r"delete", method, re.IGNORECASE) or method is HTTPMethod.DELETE:
            response = await self.delete(url, *args, **kwargs)
        elif re.search(r"head", method, re.IGNORECASE) or method is HTTPMethod.HEAD:
            response = await self.head(url, *args, **kwargs)
        elif re.search(r"option", method, re.IGNORECASE) or method is HTTPMethod.OPTION:
            response = await self.option(url, *args, **kwargs)
        else:
            response = TypeError(f"Invalid HTTP method it got: '{method.upper()}'.")
        return response


    async def get(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        return None


    async def post(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        return None


    async def put(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        return None


    async def delete(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        return None


    async def head(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        return None


    async def option(self, url: str, *args, **kwargs) -> Generic[HTTPResponse]:
        return None


    @property
    def __before_request(self) -> Callable:
        return self.before_request


    @property
    def __request_done(self) -> Callable:
        return self.request_done


    @property
    def __request_error(self) -> Callable:
        return self.request_fail


    @property
    def __request_final(self) -> Callable:
        return self.request_final


    async def before_request(self, *args, **kwargs) -> None:
        """
        Asynchronous version of *HTTP.before_request*.

        :return: None
        """

        pass


    async def request_done(self, result):
        """
        Asynchronous version of *HTTP.request_done*.

        :param result: The result of sending HTTP request. In generally, it's HTTP response object.
        :return: The handled result.
        """

        return result


    async def request_fail(self, error: Exception) -> None:
        """
        Asynchronous version of *HTTP.request_fail*.

        :param error:
        :return: None
        """

        raise error


    async def request_final(self) -> None:
        """
        Asynchronous version of *HTTP.request_final*.

        :return: None
        """

        pass


    def status_code(self):
        pass


