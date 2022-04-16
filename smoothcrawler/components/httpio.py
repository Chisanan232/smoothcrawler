from multirunnable.api import retry as _retry, async_retry as _async_retry
from typing import Callable, Any
from abc import ABCMeta, abstractmethod
import re



class BaseHTTP(metaclass=ABCMeta):

    def __init__(self):
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


    @abstractmethod
    def status_code(self):
        pass



class HTTP(BaseHTTP):

    def __init__(self):
        super().__init__()


    def request(self,
                url: str,
                method: str = "GET",
                timeout: int = 1,
                *args, **kwargs):

        _self = self

        @_retry.function(timeout=timeout)
        def __retry_request_process(_method: str = "GET", _timeout: int = 1, *_args, **_kwargs):
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
                          method: str = "GET",
                          timeout: int = 1,
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


    def before_request(self, *args, **kwargs):
        pass


    def request_done(self, result):
        return result


    def request_fail(self, error: Exception):
        raise error


    def request_final(self):
        pass


    def status_code(self):
        pass



class AsyncHTTP(BaseHTTP):

    def __init__(self):
        super().__init__()


    async def request(self,
                      url: str,
                      method: str = "GET",
                      timeout: int = 1,
                      *args, **kwargs):

        _self = self

        @_async_retry.function(timeout=timeout)
        async def __async_retry_request_process(_self, _method: str = "GET", _timeout: int = 1, *_args, **_kwargs):
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
                                method: str = "GET",
                                timeout: int = 1,
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


    async def before_request(self, *args, **kwargs):
        pass


    async def request_done(self, result):
        return result


    async def request_fail(self, error: Exception):
        raise error


    async def request_final(self):
        pass


    def status_code(self):
        pass


