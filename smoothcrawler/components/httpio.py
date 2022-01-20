from abc import ABCMeta, abstractmethod
from types import MethodType, FunctionType, CoroutineType
from typing import Callable, Coroutine, Optional, Union, Type, Any
from multirunnable.api import retry as _retry, async_retry as _async_retry
import re


RETRY_TIME: int = 1


def set_retry(times: int) -> None:
    global RETRY_TIME
    RETRY_TIME = times


def get_retry() -> int:
    return RETRY_TIME


class BaseRetryComponent(metaclass=ABCMeta):

    @abstractmethod
    def before_request(self, *args, **kwargs) -> None:
        pass


    @abstractmethod
    def request_done(self, result):
        return result


    @abstractmethod
    def request_final(self) -> None:
        pass


    @abstractmethod
    def request_error(self, error: Exception):
        return error



class RetryComponent(BaseRetryComponent):

    def before_request(self, *args, **kwargs) -> None:
        pass


    def request_done(self, result):
        return result


    def request_final(self) -> None:
        pass


    def request_error(self, error: Exception):
        raise error



class AsyncRetryComponent(BaseRetryComponent):

    async def before_request(self, *args, **kwargs) -> None:
        pass


    async def request_done(self, result):
        return result


    async def request_final(self) -> None:
        pass


    async def request_error(self, error: Exception):
        raise error



class BaseHTTP(metaclass=ABCMeta):

    def __init__(self, retry_components: BaseRetryComponent = None):
        pass


    @abstractmethod
    def request(self, url: str, method: str = "GET", timeout: int = -1, *args, **kwargs):
        pass


    @abstractmethod
    def get(self, url: str, *args, **kwargs):
        pass


    @abstractmethod
    def post(self, url: str, *args, **kwargs):
        pass


    @abstractmethod
    def put(self, url: str, *args, **kwargs):
        pass


    @abstractmethod
    def delete(self, url: str, *args, **kwargs):
        pass


    @abstractmethod
    def head(self, url: str, *args, **kwargs):
        pass


    @abstractmethod
    def option(self, url: str, *args, **kwargs):
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

    __Retry_Mechanism_Default_Functions = RetryComponent()
    _Before_Request_Callable: Callable = None
    _Request_Done_Callable: Callable = None
    _Request_Final_Callable: Callable = None
    _Error_Request_Callable: Callable = None

    def __init__(self, retry_components: BaseRetryComponent = None):
        super().__init__(retry_components)
        if retry_components is not None:
            if not isinstance(retry_components, BaseRetryComponent):
                raise TypeError("Parameter *retry_components* should be a sub-class of 'smoothcrawler.http_io.RetryComponent'.")
            self.__Retry_Mechanism_Default_Functions = retry_components


    def request(self,
                url: str,
                method: str = "GET",
                timeout: int = -1,
                retry_components: BaseRetryComponent = None,
                *args, **kwargs):

        _self = self

        @_retry(timeout=RETRY_TIME)
        def _request(_self, _method: str = "GET", _timeout: int = -1, *_args, **_kwargs):
            _response = self.__request_process(url=url, method=_method, timeout=_timeout, *_args, **_kwargs)
            return _response

        @_request.initialization
        def _before_request(_self, *_args, **_kwargs) -> None:
            self.before_request(*_args, **_kwargs)

        @_request.done_handling
        def _request_done(_self, result):
            __result = self.request_done(result)
            return __result

        @_request.final_handling
        def _request_final(_self) -> None:
            self.request_final()

        @_request.error_handling
        def _request_error(_self, error: Exception):
            __error_handle = self.request_error(error)
            return __error_handle

        response = _request(self, method, timeout, *args, **kwargs)
        if response is TypeError and str(response) == f"Invalid HTTP method it got: '{method}'.":
            raise response
        return response


    def __request_process(self,
                          url: str,
                          method: str = "GET",
                          timeout: int = -1,
                          *args, **kwargs) -> Any:
        if re.search(f"get", method, re.IGNORECASE):
            response = self.get(url, *args, **kwargs)
        elif re.search(f"post", method, re.IGNORECASE):
            response = self.post(url, *args, **kwargs)
        elif re.search(f"put", method, re.IGNORECASE):
            response = self.put(url, *args, **kwargs)
        elif re.search(f"delete", method, re.IGNORECASE):
            response = self.delete(url, *args, **kwargs)
        elif re.search(f"head", method, re.IGNORECASE):
            response = self.head(url, *args, **kwargs)
        elif re.search(f"option", method, re.IGNORECASE):
            response = self.option(url, *args, **kwargs)
        else:
            response = TypeError(f"Invalid HTTP method it got: '{method.upper()}'.")
        return response


    def get(self, url: str, *args, **kwargs):
        return None


    def post(self, url: str, *args, **kwargs):
        return None


    def put(self, url: str, *args, **kwargs):
        return None


    def delete(self, url: str, *args, **kwargs):
        return None


    def head(self, url: str, *args, **kwargs):
        return None


    def option(self, url: str, *args, **kwargs):
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

    __Retry_Mechanism_Default_Functions = AsyncRetryComponent()
    _Before_Request_Callable: Callable = None
    _Request_Done_Callable: Callable = None
    _Request_Final_Callable: Callable = None
    _Error_Request_Callable: Callable = None

    def __init__(self, retry_components: BaseRetryComponent = None):
        super().__init__(retry_components)
        if retry_components is not None:
            if isinstance(retry_components, BaseRetryComponent):
                raise TypeError("Parameter *retry_components* should be a sub-class of 'smoothcrawler.http_io.AsyncRetryComponent'.")
            self.__Retry_Mechanism_Default_Functions = retry_components


    async def request(self,
                      url: str,
                      method: str = "GET",
                      timeout: int = -1,
                      *args, **kwargs):

        _self = self

        @_async_retry(timeout=RETRY_TIME)
        async def _request(_self, _method: str = "GET", _timeout: int = -1, *_args, **_kwargs):
            __response = await _self.__request_process(url=url, method=_method, timeout=_timeout, *_args, **_kwargs)
            return __response

        @_request.initialization
        async def _before_request(_self, *_args, **_kwargs):
            await self.before_request(*_args, **_kwargs)

        @_request.done_handling
        async def _request_done(_self, result):
            __result = await self.request_done(result)
            return __result

        @_request.final_handling
        async def _request_final(_self):
            await self.request_final()

        @_request.error_handling
        async def _request_error(_self, error):
            __error_handle = await self.request_error(error)
            return __error_handle

        response = await _request(self, method, timeout, *args, **kwargs)
        if response is TypeError and str(response) == f"Invalid HTTP method it got: '{method}'.":
            raise response
        return response


    async def __request_process(self,
                                url: str,
                                method: str = "GET",
                                timeout: int = -1,
                                *args, **kwargs):
        if re.search(f"get", method, re.IGNORECASE):
            response = await self.get(url, *args, **kwargs)
        elif re.search(f"post", method, re.IGNORECASE):
            response = await self.post(url, *args, **kwargs)
        elif re.search(f"put", method, re.IGNORECASE):
            response = await self.put(url, *args, **kwargs)
        elif re.search(f"delete", method, re.IGNORECASE):
            response = await self.delete(url, *args, **kwargs)
        elif re.search(f"head", method, re.IGNORECASE):
            response = await self.head(url, *args, **kwargs)
        elif re.search(f"option", method, re.IGNORECASE):
            response = await self.option(url, *args, **kwargs)
        else:
            response = TypeError(f"Invalid HTTP method it got: '{method.upper()}'.")
        return response


    async def get(self, url: str, *args, **kwargs):
        return None


    async def post(self, url: str, *args, **kwargs):
        return None


    async def put(self, url: str, *args, **kwargs):
        return None


    async def delete(self, url: str, *args, **kwargs):
        return None


    async def head(self, url: str, *args, **kwargs):
        return None


    async def option(self, url: str, *args, **kwargs):
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


    def status_code(self):
        pass


