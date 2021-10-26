from multirunnable.api import retry as _retry, async_retry as _async_retry

from abc import ABCMeta, abstractmethod
from typing import Callable, Optional, Union
import re


RETRY_TIME: int = 1


def set_retry(times: int) -> None:
    global RETRY_TIME
    RETRY_TIME = times


def get_retry() -> int:
    return RETRY_TIME


class RetryFunctionComponent:

    def before_request(self, *args, **kwargs) -> None:
        pass


    def request_done(self, result):
        return result


    def request_final(self) -> None:
        pass


    def request_error(self, error: Exception):
        return error


    async def async_before_request(self, *args, **kwargs) -> None:
        pass


    async def async_request_done(self, result):
        return result


    async def async_request_final(self) -> None:
        pass


    async def async_request_error(self, error: Exception):
        return error



class BaseHTTP(metaclass=ABCMeta):

    @abstractmethod
    def request(self, method: str = "GET", timeout: int = -1, *args, **kwargs):
        pass


    @abstractmethod
    def get(self, *args, **kwargs):
        pass


    @abstractmethod
    def post(self, *args, **kwargs):
        pass


    @abstractmethod
    def put(self, *args, **kwargs):
        pass


    @abstractmethod
    def delete(self, *args, **kwargs):
        pass


    @abstractmethod
    def head(self, *args, **kwargs):
        pass


    @abstractmethod
    def option(self, *args, **kwargs):
        pass


    @property
    @abstractmethod
    def before_request(self) -> Callable:
        pass


    @property
    @abstractmethod
    def request_done(self) -> Callable:
        pass


    @property
    @abstractmethod
    def request_final(self) -> Callable:
        pass


    @property
    @abstractmethod
    def request_error(self) -> Callable:
        pass


    @abstractmethod
    def status_code(self):
        pass



class HTTP(BaseHTTP):

    __Retry_Mechanism_Default_Functions = RetryFunctionComponent()
    _Before_Request_Callable: Callable = None
    _Request_Done_Callable: Callable = None
    _Request_Final_Callable: Callable = None
    _Error_Request_Callable: Callable = None

    def __init__(self, retry_components: RetryFunctionComponent = None):
        if retry_components is not None:
            if type(retry_components) is not RetryFunctionComponent:
                raise TypeError("Parameter *retry_components* should be a sub-class of 'smoothcrawler.http_io.RetryFunctionComponent'.")
            self.__Retry_Mechanism_Default_Functions = retry_components


    def request(self,
                method: str = "GET",
                timeout: int = -1,
                retry_components: RetryFunctionComponent = None,
                *args, **kwargs):

        _self = self

        @_retry(timeout=RETRY_TIME)
        def __request(_self, _method: str = "GET", _timeout: int = -1, *_args, **_kwargs):
            __response = _self.__request_process(method=_method, timeout=_timeout, *_args, **_kwargs)
            return __response

        @__request.initialization
        def __before_request(_self, *_args, **_kwargs):
            self.before_request(*_args, **_kwargs)

        @__request.done_handling
        def __request_done(_self, result):
            __result = self.request_done(result)
            return __result

        @__request.final_handling
        def __request_final(_self):
            self.request_final()

        @__request.error_handling
        def __request_error(_self, error):
            __error_handle = self.request_error(error)
            return __error_handle

        return __request(self, method, timeout, *args, **kwargs)


    def __request_process(self,
                          method: str = "GET",
                          timeout: int = -1,
                          *args, **kwargs):
        if re.search(f"get", method, re.IGNORECASE):
            response = self.get(*args, **kwargs)
        elif re.search(f"post", method, re.IGNORECASE):
            response = self.post(*args, **kwargs)
        elif re.search(f"put", method, re.IGNORECASE):
            response = self.put(*args, **kwargs)
        elif re.search(f"delete", method, re.IGNORECASE):
            response = self.delete(*args, **kwargs)
        elif re.search(f"head", method, re.IGNORECASE):
            response = self.head(*args, **kwargs)
        elif re.search(f"option", method, re.IGNORECASE):
            response = self.option(*args, **kwargs)
        else:
            raise TypeError(f"Invalid HTTP method it got: '{method.upper()}'.")
        return response


    def get(self, *args, **kwargs):
        return None


    def post(self, *args, **kwargs):
        return None


    def put(self, *args, **kwargs):
        return None


    def delete(self, *args, **kwargs):
        return None


    def head(self, *args, **kwargs):
        return None


    def option(self, *args, **kwargs):
        return None


    @property
    def before_request(self) -> Callable:
        if self._Before_Request_Callable is None:
            return self.__Retry_Mechanism_Default_Functions.before_request
        return self._Before_Request_Callable


    @before_request.setter
    def before_request(self, function: Callable) -> None:
        self._Before_Request_Callable = function


    @property
    def request_done(self) -> Callable:
        if self._Request_Done_Callable is None:
            return self.__Retry_Mechanism_Default_Functions.request_done
        return self._Request_Done_Callable


    @request_done.setter
    def request_done(self, function: Callable) -> None:
        self._Request_Done_Callable = function


    @property
    def request_final(self) -> Callable:
        if self._Request_Final_Callable is None:
            return self.__Retry_Mechanism_Default_Functions.request_final
        return self._Request_Final_Callable


    @request_final.setter
    def request_final(self, function: Callable) -> None:
        self._Request_Final_Callable = function


    @property
    def request_error(self) -> Callable:
        if self._Error_Request_Callable is None:
            return self.__Retry_Mechanism_Default_Functions.request_error
        return self._Error_Request_Callable


    @request_error.setter
    def request_error(self, function: Callable) -> None:
        self._Error_Request_Callable = function


    def response(self):
        pass


    def status_code(self):
        pass



class AsyncHTTP(BaseHTTP):

    __Retry_Mechanism_Default_Functions = RetryFunctionComponent()
    _Before_Request_Callable: Callable = None
    _Request_Done_Callable: Callable = None
    _Request_Final_Callable: Callable = None
    _Error_Request_Callable: Callable = None

    async def request(self,
                      method: str = "GET",
                      timeout: int = -1,
                      *args, **kwargs):

        _self = self

        @_async_retry(timeout=RETRY_TIME)
        async def __request(_self, _method: str = "GET", _timeout: int = -1, *_args, **_kwargs):
            __response = await _self.__request_process(method=_method, timeout=_timeout, *_args, **_kwargs)
            return __response

        @__request.initialization
        async def __before_request(_self, *_args, **_kwargs):
            await self.before_request(*_args, **_kwargs)

        @__request.done_handling
        async def __request_done(_self, result):
            __result = await self.request_done(result)
            return __result

        @__request.final_handling
        async def __request_final(_self):
            await self.request_final()

        @__request.error_handling
        async def __request_error(_self, error):
            __error_handle = await self.request_error(error)
            return __error_handle

        return await __request(self, method, timeout, *args, **kwargs)


    async def __request_process(self,
                                method: str = "GET",
                                timeout: int = -1,
                                *args, **kwargs):
        if re.search(f"get", method, re.IGNORECASE):
            response = await self.get(*args, **kwargs)
        elif re.search(f"post", method, re.IGNORECASE):
            response = await self.post(*args, **kwargs)
        elif re.search(f"put", method, re.IGNORECASE):
            response = await self.put(*args, **kwargs)
        elif re.search(f"delete", method, re.IGNORECASE):
            response = await self.delete(*args, **kwargs)
        elif re.search(f"head", method, re.IGNORECASE):
            response = await self.head(*args, **kwargs)
        elif re.search(f"option", method, re.IGNORECASE):
            response = await self.option(*args, **kwargs)
        else:
            raise TypeError(f"Invalid HTTP method it got: '{method.upper()}'.")
        return response


    async def get(self, *args, **kwargs):
        return None


    async def post(self, *args, **kwargs):
        return None


    async def put(self, *args, **kwargs):
        return None


    async def delete(self, *args, **kwargs):
        return None


    async def head(self, *args, **kwargs):
        return None


    async def option(self, *args, **kwargs):
        return None


    @property
    def before_request(self) -> Callable:
        if self._Before_Request_Callable is None:
            return self.__Retry_Mechanism_Default_Functions.async_before_request
        return self._Before_Request_Callable


    @before_request.setter
    def before_request(self, function: Callable) -> None:
        self._Before_Request_Callable = function


    @property
    def request_done(self) -> Callable:
        if self._Request_Done_Callable is None:
            return self.__Retry_Mechanism_Default_Functions.async_request_done
        return self._Request_Done_Callable


    @request_done.setter
    def request_done(self, function: Callable) -> None:
        self._Request_Done_Callable = function


    @property
    def request_final(self) -> Callable:
        if self._Request_Final_Callable is None:
            return self.__Retry_Mechanism_Default_Functions.async_request_final
        return self._Request_Final_Callable


    @request_final.setter
    def request_final(self, function: Callable) -> None:
        self._Request_Final_Callable = function


    @property
    def request_error(self) -> Callable:
        if self._Error_Request_Callable is None:
            return self.__Retry_Mechanism_Default_Functions.async_request_error
        return self._Error_Request_Callable


    @request_error.setter
    def request_error(self, function: Callable) -> None:
        self._Error_Request_Callable = function


    def status_code(self):
        pass


