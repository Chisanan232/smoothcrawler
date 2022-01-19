from smoothcrawler.factory import CrawlerFactory
from smoothcrawler.components.httpio import (
    set_retry as _set_retry,
    BaseHTTP as _BaseHttpIo,
    BaseRetryComponent as _BaseRetryComponent
)
from smoothcrawler.components.data import (
    BaseHTTPResponseParser as _BaseHTTPResponseParser,
    BaseDataHandler as _BaseDataHandler
)
from smoothcrawler.persistence import PersistenceFacade as _PersistenceFacade

from abc import ABCMeta, abstractmethod
from queue import Queue
from typing import List, Iterable, Any, Union, Optional, Deque, Sequence
from multirunnable import (
    RunningMode,
    SimpleExecutor,
    SimplePool
)
from multirunnable.adapter import Lock, BoundedSemaphore
from multipledispatch import dispatch
import logging



class BaseCrawler(metaclass=ABCMeta):

    _HTTP_IO: _BaseHttpIo = None
    _HTTP_Response_Parser: _BaseHTTPResponseParser = None
    _Data_Handler: _BaseDataHandler = None
    _Persistence: _PersistenceFacade = None

    def __init__(self, factory: CrawlerFactory):
        self._factory = factory


    def crawl(self,
              url: str,
              method: str,
              retry: int = 1,
              *args, **kwargs) -> Any:
        _set_retry(times=retry)
        response = self._factory.http_factory.request(method=method, url=url, *args, **kwargs)
        parsed_response = self._factory.parser_factory.parse_content(response=response)
        return parsed_response



class SimpleCrawler(BaseCrawler):

    @dispatch(str, str)
    def run(self, method: str, url: str) -> Optional[Any]:
        parsed_response = self.crawl(method=method, url=url)
        data = self._factory.data_handling_factory.process(result=parsed_response)
        return data


    @dispatch(str, list)
    def run(self, method: str, url: List[str]) -> Optional[List]:
        result = []
        for _target_url in url:
            parsed_response = self.crawl(method=method, url=_target_url)
            data = self._factory.data_handling_factory.process(result=parsed_response)
            result.append(data)
        return result


    def run_and_save(self, method: str, url: Union[str, list]) -> None:
        _result = self.run(method, url)
        self._factory.persistence_factory.save(data=_result)



class MultiRunnableCrawler(BaseCrawler):

    _Persistence_Factory = None

    @property
    def persistence_factory(self):
        return self._Persistence_Factory


    @persistence_factory.setter
    def persistence_factory(self, factory):
        self._Persistence_Factory = factory


    def process_with_list(self,
                          method: str,
                          url: List[str],
                          retry: int = 1,
                          *args, **kwargs) -> Any:
        """
        Description:
            Handling the crawler process with List which saving URLs.
        :param method:
        :param url:
        :param retry:
        :param args:
        :param kwargs:
        :return:
        """
        _set_retry(times=retry)
        for _target_url in url:
            parsed_response = self.crawl(method=method, url=_target_url)
            handled_data = self._factory.data_handling_factory.process(result=parsed_response)


    def process_with_queue(self,
                           method: str,
                           url: Queue,
                           retry: int = 1,
                           *args, **kwargs) -> Any:
        """
        Description:
            Handling the crawler process with Queue which saving URLs.
        :param method:
        :param url:
        :param retry:
        :param args:
        :param kwargs:
        :return:
        """
        _set_retry(times=retry)
        while url.empty() is False:
            _target_url = url.get()
            parsed_response = self.crawl(method=method, url=_target_url)
            handled_data = self._factory.data_handling_factory.process(result=parsed_response)


    @staticmethod
    def _get_lock_feature(lock: bool = True, sema_value: int = 1):
        """
        Description:
            Initialize Lock or Semaphore. Why? because of persistence process.
        :param lock:
        :param sema_value:
        :return:
        """
        if lock is True:
            feature = Lock()
        else:
            if sema_value <= 0:
                raise ValueError("The number of Semaphore cannot less than or equal to 0.")
            feature = BoundedSemaphore(value=sema_value)
        return feature


    @staticmethod
    def _divide_urls(urls: List[str], executor_number: int) -> List[List[str]]:
        """
        Description:
            Divide the data list which saving URLs to be a list saving multiple lists.
        :param urls:
        :param executor_number:
        :return:
        """
        urls_len = len(urls)
        urls_interval = int(urls_len / executor_number)
        urls_list_collection = [urls[i:i + urls_interval] for i in range(0, executor_number, urls_interval)]
        return urls_list_collection



class ExecutorCrawler(MultiRunnableCrawler):

    def __init__(self, mode: RunningMode, executors: int, factory: CrawlerFactory):
        super(ExecutorCrawler, self).__init__(factory=factory)
        self.__executor_number = executors
        self.__executor = SimpleExecutor(mode=mode, executors=executors)


    def run(self, method: str, url: Union[List[str], Queue], retry: int = 1, lock: bool = True, sema_value: int = 1) -> Optional:
        feature = MultiRunnableCrawler._get_lock_feature(lock=lock, sema_value=sema_value)

        if type(url) is list:
            urls_len = len(url)
            if urls_len <= self.__executor_number:
                logging.warning(f"It will have some idle executors deosn't be activated because target URLs amount more than executor number.")
                logging.warning(f"URLs amount: {urls_len}")
                logging.warning(f"Executor number: {self.__executor_number}")
                _result = self.map(method=method, url=url, retry=retry, lock=lock, sema_value=sema_value)
                return _result
            else:
                urls_list_collection = MultiRunnableCrawler._divide_urls(urls=url, executor_number=self.__executor_number)

                self.__executor.run(
                    function=self.process_with_list,
                    args={"method": method, "url": urls_list_collection, "retry": retry},
                    queue_tasks=None,
                    features=feature)
        else:
            self.__executor.run(
                function=self.process_with_queue,
                args={"method": method, "url": url, "retry": retry},
                queue_tasks=None,
                features=feature)

        result = self.__executor.result()
        return result


    def map(self, method: str, url: List[str], retry: int = 1, lock: bool = True, sema_value: int = 1) -> Optional:
        feature = MultiRunnableCrawler._get_lock_feature(lock=lock, sema_value=sema_value)
        args_iterator = [{"method": method, "url": _url, "retry": retry} for _url in url]

        self.__executor.map(
            function=self.crawl,
            args_iter=args_iterator,
            queue_tasks=None,
            features=feature)
        result = self.__executor.result()
        return result



class AsyncSimpleCrawler(MultiRunnableCrawler):

    def __init__(self, executors: int, factory: CrawlerFactory):
        super(AsyncSimpleCrawler, self).__init__(factory=factory)
        self.__executor_number = executors
        self.__executor = SimpleExecutor(mode=RunningMode.Asynchronous, executors=executors)


    async def crawl(self,
                    url: str,
                    method: str,
                    retry: int = 1,
                    *args, **kwargs) -> Any:
        _set_retry(times=retry)
        response = await self._factory.http_factory.request(method=method, url=url, *args, **kwargs)
        parsed_response = await self._factory.parser_factory.parse_content(response=response)
        return parsed_response


    async def process_with_list(self,
                                method: str,
                                url: List[str],
                                retry: int = 1,
                                *args, **kwargs) -> Any:
        """
        Description:
            Handling the crawler process with List which saving URLs.
        :param method:
        :param url:
        :param retry:
        :param args:
        :param kwargs:
        :return:
        """
        _set_retry(times=retry)
        for _target_url in url:
            parsed_response = await self.crawl(method=method, url=_target_url)
            handled_data = await self._factory.data_handling_factory.process(result=parsed_response)


    async def process_with_queue(self,
                                 method: str,
                                 url: Queue,
                                 retry: int = 1,
                                 *args, **kwargs) -> Any:
        """
        Description:
            Handling the crawler process with Queue which saving URLs.
        :param method:
        :param url:
        :param retry:
        :param args:
        :param kwargs:
        :return:
        """
        _set_retry(times=retry)
        while url.empty() is False:
            _target_url = await url.get()
            parsed_response = await self.crawl(method=method, url=_target_url)
            handled_data = await self._factory.data_handling_factory.process(result=parsed_response)


    def run(self, method: str, url: Union[List[str], Queue], retry: int = 1, lock: bool = True, sema_value: int = 1) -> Optional:
        feature = MultiRunnableCrawler._get_lock_feature(lock=lock, sema_value=sema_value)

        if type(url) is list:
            urls_list_collection = MultiRunnableCrawler._divide_urls(urls=url, executor_number=self.__executor_number)
            self.__executor.run(
                function=self.process_with_list,
                args={"method": method, "url": urls_list_collection, "retry": retry},
                queue_tasks=None,
                features=feature)
        else:
            self.__executor.run(
                function=self.process_with_queue,
                args={"method": method, "url": url, "retry": retry},
                queue_tasks=None,
                features=feature)

        result = self.__executor.result()
        return result



class PoolCrawler(MultiRunnableCrawler):

    def __init__(self, mode: RunningMode, pool_size: int, tasks_size: int, factory: CrawlerFactory):
        super(PoolCrawler, self).__init__(factory=factory)
        self.__pool = SimplePool(mode=mode, pool_size=pool_size, tasks_size=tasks_size)


    def __enter__(self):
        self.init()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def init(self, lock: bool = True, sema_value: int = 1) -> None:
        """
        Description:
            Initialize something which be needed before new Pool object.
        :param lock:
        :param sema_value:
        :return:
        """
        feature = MultiRunnableCrawler._get_lock_feature(lock=lock, sema_value=sema_value)
        self.__pool.initial(queue_tasks=None, features=feature)


    def apply(self, method: str, url: str, retry: int = 1) -> Optional:
        _kwargs = {"method": method, "url": url, "retry": retry}
        self.__pool.apply(function=self.crawl, **_kwargs)
        result = self.__pool.get_result()
        return result


    def async_apply(self, method: str, url: str, retry: int = 1) -> Optional:
        _kwargs = {"method": method, "url": url, "retry": retry}
        self.__pool.async_apply(
            function=self.crawl,
            kwargs=_kwargs,
            callback=None,
            error_callback=None)
        result = self.__pool.get_result()
        return result


    def map(self, method: str, url: str, retry: int = 1) -> Optional:
        _kwargs = {"method": method, "url": url, "retry": retry}
        self.__pool.map(function=self.crawl, **_kwargs)
        result = self.__pool.get_result()
        return result


    def async_map(self, method: str, url: str, retry: int = 1) -> Optional:
        _kwargs = {"method": method, "url": url, "retry": retry}
        self.__pool.async_map(function=self.crawl, **_kwargs)
        result = self.__pool.get_result()
        return result


    def terminal(self) -> None:
        self.__pool.terminal()


    def close(self) -> None:
        self.__pool.close()

