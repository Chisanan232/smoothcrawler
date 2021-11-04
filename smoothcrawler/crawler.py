from smoothcrawler.httpio import (
    set_retry as _set_retry,
    BaseHTTP as _BaseHttpIo,
    BaseRetryComponent as _BaseRetryComponent
)
from smoothcrawler.data import (
    BaseHTTPResponseParser as _BaseHTTPResponseParser,
    BaseDataHandler as _BaseDataHandler
)
from smoothcrawler.persistence.file import PersistenceFacade as _PersistenceFacade

from multirunnable import (
    RunningMode,
    SimpleExecutor,
    PersistenceExecutor,
    SimplePool,
    PersistencePool
)
from multirunnable.adapter import Lock, BoundedSemaphore

from abc import ABCMeta, abstractmethod
from typing import Iterable, Any, Union, Optional



class BaseCrawler(metaclass=ABCMeta):

    _HTTP_IO: _BaseHttpIo = None
    _HTTP_Response_Parser: _BaseHTTPResponseParser = None
    _Data_Handler: _BaseDataHandler = None
    _Persistence: _PersistenceFacade = None

    @property
    def http_io(self) -> _BaseHttpIo:
        if self._HTTP_IO is None:
            raise ValueError("Factory 'HTTP_IO' can not be empty.")
        return self._HTTP_IO


    @http_io.setter
    def http_io(self, http_io) -> None:
        self._HTTP_IO = http_io


    @property
    def http_response_parser(self) -> _BaseHTTPResponseParser:
        if self._HTTP_Response_Parser is None:
            raise ValueError("Factory 'HTTP_Response_Parser' can not be empty.")
        return self._HTTP_Response_Parser


    @http_response_parser.setter
    def http_response_parser(self, parser) -> None:
        self._HTTP_Response_Parser = parser


    @property
    def data_handler(self) -> _BaseDataHandler:
        if self._Data_Handler is None:
            raise ValueError("Factory 'Data_Handler' can not be empty.")
        return self._Data_Handler


    @data_handler.setter
    def data_handler(self, data_handler) -> None:
        self._Data_Handler = data_handler


    @property
    def persistence(self) -> _PersistenceFacade:
        if self._Persistence is None:
            raise ValueError("Factory 'Persistence' can not be empty.")
        return self._Persistence


    @persistence.setter
    def persistence(self, persistence) -> None:
        self._Persistence = persistence


    def crawl(self,
              url: str,
              method: str,
              retry: int = 1,
              *args, **kwargs) -> Any:
        _set_retry(times=retry)
        response = self.http_io.request(method=method, url=url, *args, **kwargs)
        parsed_response = self.http_response_parser.parse_content(response=response)
        return parsed_response


    def request(self):
        pass


    def parse(self):
        pass



class SimpleCrawler(BaseCrawler):

    def run(self, method: str, url: str, retry: int = 1, file: str = "") -> Optional:
        parsed_response = self.crawl(method=method, url=url, retry=retry)
        data = self.data_handler.process(result=parsed_response)
        if file is not "":
            self.persistence.save_as_file(file=file, mode="a+", data=data)
        return data



class BaseMultiRunnableCrawler(BaseCrawler):

    @staticmethod
    def _get_lock_feature(lock: bool = True, sema_value: int = 1):
        if lock is True:
            feature = Lock()
        else:
            if sema_value <= 0:
                raise ValueError("The number of Semaphore cannot less than or equal to 0.")
            feature = BoundedSemaphore(value=sema_value)
        return feature



class ExecutorCrawler(BaseMultiRunnableCrawler):

    def __init__(self, mode: RunningMode, executors: int):
        self.__executor_number = executors
        self.__executor = SimpleExecutor(mode=mode, executors=executors)


    def run(self, method: str, url: str, retry: int = 1, file: str = "", lock: bool = True, sema_value: int = 1) -> Optional:
        feature = BaseMultiRunnableCrawler._get_lock_feature(lock=lock, sema_value=sema_value)

        self.__executor.run(
            function=self.crawl,
            args={"method": method, "url": url, "retry": retry, "file": file},
            queue_tasks=None,
            features=feature)
        result = self.__executor.result()
        return result


    # def map(self, method: str, url: str, retry: int = 1, file: str = "") -> Optional:
    #     self.__executor.map()



class AsyncSimpleCrawler(BaseCrawler):

    def run(self, method: str, url: str, retry: int = 1, file: str = "") -> Optional:
        pass



class PoolCrawler(BaseMultiRunnableCrawler):

    def __init__(self, mode, pool_size, tasks_size):
        self.__pool = SimplePool(mode=mode, pool_size=pool_size, tasks_size=tasks_size)


    def __enter__(self):
        self.init()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def init(self, lock: bool = True, sema_value: int = 1) -> None:
        feature = BaseMultiRunnableCrawler._get_lock_feature(lock=lock, sema_value=sema_value)
        self.__pool.initial(queue_tasks=None, features=feature)


    def apply(self, method: str, url: str, retry: int = 1, file: str = "") -> Optional:
        _kwargs = {"method": method, "url": url, "retry": retry, "file": file}
        self.__pool.apply(function=self.crawl, **_kwargs)
        result = self.__pool.get_result()
        return result


    def async_apply(self, method: str, url: str, retry: int = 1, file: str = "") -> Optional:
        _kwargs = {"method": method, "url": url, "retry": retry, "file": file}
        self.__pool.async_apply(
            function=self.crawl,
            kwargs=_kwargs,
            callback=None,
            error_callback=None)
        result = self.__pool.get_result()
        return result


    def terminal(self) -> None:
        self.__pool.terminal()


    def close(self) -> None:
        self.__pool.close()



class CrazyCrawler(BaseMultiRunnableCrawler):

    def __init__(self):
        # Get the resource info of the running environment
        mode = RunningMode.Parallel
        pool_size = 1
        tasks_size = 1
        SimplePool(mode=mode, pool_size=pool_size, tasks_size=tasks_size)


    def run(self, method: str, url: str, retry: int = 1, file: str = "") -> Optional:
        pass


