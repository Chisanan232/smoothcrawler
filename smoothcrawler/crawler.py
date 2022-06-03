from multipledispatch import dispatch
from multirunnable.factory import LockFactory, BoundedSemaphoreFactory
from multirunnable import RunningMode, SimpleExecutor, SimplePool
from typing import List, Iterable, Any, TypeVar, Union, Optional, Generic, Callable
from queue import Queue
from abc import ABCMeta
import logging

from .components.persistence import PersistenceFacade as _PersistenceFacade
from .components.httpio import BaseHTTP as _BaseHttpIo
from .components.data import (
    BaseHTTPResponseParser as _BaseHTTPResponseParser,
    BaseDataHandler as _BaseDataHandler,
    BaseAsyncDataHandler as _BaseAsyncDataHandler
)
from .factory import BaseFactory, CrawlerFactory, AsyncCrawlerFactory


RunAsParallel = RunningMode.Parallel
RunAsConcurrent = RunningMode.Concurrent
RunAsCoroutine = RunningMode.GreenThread

T = TypeVar("T")


class BaseCrawler(metaclass=ABCMeta):

    _HTTP_IO: _BaseHttpIo = None
    _HTTP_Response_Parser: _BaseHTTPResponseParser = None
    _Data_Handler: _BaseDataHandler = None
    _Persistence: _PersistenceFacade = None

    def __init__(self, factory: BaseFactory = None):
        """
        Define some basically functions to all crawlers.

        :param factory: The BaseFactory object which would provides each different factories to
        crawler uses like send HTTP request, parse HTTP response, etc.
        """

        if factory is None:
            self._factory = self._initial_factory()
        else:
            self._factory = factory


    def _initial_factory(self) -> BaseFactory:
        """
        Initial BaseFactory object. This function would be called if value of option *factory* of __init__ is None.

        :return: CrawlerFactory instance.
        """

        return CrawlerFactory()


    def register_factory(self,
                         http_req_sender: _BaseHttpIo = None,
                         http_resp_parser: _BaseHTTPResponseParser = None,
                         data_process: Union[_BaseDataHandler, _BaseAsyncDataHandler] = None,
                         persistence: _PersistenceFacade = None) -> None:
        """
        Register SmoothCrawler's component(s) to CrawlerFactory instance.

        :param http_req_sender: The *Sender* component sends HTTP request.
        :param http_resp_parser: The *Parser* component handles HTTP response.
        :param data_process: The *Handler* component handles data process which be generated from HTTP response.
        :param persistence: The *Persistence* component response of saving data.
        :return: None
        """

        self._factory.http_factory = http_req_sender
        self._factory.parser_factory = http_resp_parser
        self._factory.data_handling_factory = data_process
        self._factory.persistence_factory = persistence


    def crawl(self, method: str, url: str, retry: int = 1, *args, **kwargs) -> Any:
        """
        Crawl web data process. It would send HTTP request, receive HTTP response and
        parse the content here. It ONLY does it, doesn't do anything else.

        :param method: HTTP method.
        :param url: URL.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :return: The result which it has parsed from HTTP response. The data type is Any.
        """

        response = self.send_http_request(method=method, url=url, retry=retry, *args, **kwargs)
        parsed_response = self.parse_http_response(response=response)
        return parsed_response


    def send_http_request(self, method: str, url: str, retry: int = 1, *args, **kwargs) -> Generic[T]:
        """
        Send HTTP request.
        It could override this function to implement your own customized logic to send HTTP request.

        :param method: HTTP method.
        :param url: URL.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :return: A HTTP response object.
        """

        response = self._factory.http_factory.request(method=method, url=url, timeout=retry, *args, **kwargs)
        return response


    def parse_http_response(self, response: Generic[T]) -> Generic[T]:
        """
        Parse the HTTP response.
        It could override this function to implement your own customized logic to parse HTTP response.

        :param response: The HTTP response.
        :return: The result which it has parsed from HTTP response. The data type is Generic[T].
        """

        parsed_response = self._factory.parser_factory.parse_content(response=response)
        return parsed_response


    def data_process(self, parsed_response: Generic[T]) -> Generic[T]:
        """
        The data process to handle the data which has been parsed from HTTP response object.
        It could override this function to implement your own customized logic to do data process.

        :param parsed_response: The data which has been parsed from HTTP response object.
        :return: The result of data process. The data type is Generic[T].
        """

        data = self._factory.data_handling_factory.process(result=parsed_response)
        return data


    def persist(self, data: Any) -> None:
        """
        Persist the data.
        It could override this function to implement your own customized logic to save data.

        :param data: The target data to persist. In generally, this is the data which has been parsed and handled.
        :return: None
        """
        self._factory.persistence_factory.save(data=data)



class SimpleCrawler(BaseCrawler):

    @dispatch(str, str)
    def run(self, method: str, url: str) -> Optional[Any]:
        """
        It would crawl the data and do some data process for the parsed HTTP response object.

        :param method: HTTP method.
        :param url: URL. It only one URL here.
        :return: The result of data process.
        """

        parsed_response = self.crawl(method=method, url=url)
        data = self.data_process(parsed_response=parsed_response)
        return data


    @dispatch(str, list)
    def run(self, method: str, url: List[str]) -> Optional[List]:
        """
        This's the overload function of previous one. The only different is: this is handling
        with a collection of URLs and previous one handles only one.

        :param method: HTTP method.
        :param url: URLs. It could receive a collection of URLs.
        :return: The result of data process.
        """

        result = []
        for _target_url in url:
            parsed_response = self.crawl(method=method, url=_target_url)
            data = self.data_process(parsed_response=parsed_response)
            result.append(data)
        return result


    def run_and_save(self, method: str, url: Union[str, list]) -> None:
        """
        In addiction to crawl and handle the data from web, it persist the data.

        :param method: HTTP method.
        :param url: One or more URLs (a collection of URLs).
        :return: None
        """

        _result = self.run(method, url)
        self.persist(data=_result)



class MultiRunnableCrawler(BaseCrawler):

    _Persistence_Factory: _PersistenceFacade = None

    @property
    def persistence_factory(self) -> _PersistenceFacade:
        """
        Get the instance of persistence factory object.

        :return: A **PersistenceFacade** type object.
        """

        return self._Persistence_Factory


    @persistence_factory.setter
    def persistence_factory(self, factory: _PersistenceFacade) -> None:
        self._Persistence_Factory = factory


    def process_with_list(self, method: str, url: List[str], retry: int = 1, *args, **kwargs) -> List[Any]:
        """
        Handling the crawler process with List of URLs.

        :param method: HTTP method.
        :param url: A collection of URLs.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :return: A list of result of data process.
        """

        _handled_data = []
        for _target_url in url:
            parsed_response = self.crawl(method=method, url=_target_url)
            _handled_data_row = self.data_process(parsed_response=parsed_response)
            _handled_data.append(_handled_data_row)
        return _handled_data


    def process_with_queue(self, method: str, url: Queue, retry: int = 1, *args, **kwargs) -> List[Any]:
        """
        Handling the crawler process with Queue which saving URLs.

        :param method: HTTP method.
        :param url: Queue of URLs.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :return: A list of result of data process.
        """

        _handled_data = []
        while url.empty() is False:
            _target_url = url.get()
            parsed_response = self.crawl(method=method, url=_target_url)
            _handled_data_row = self.data_process(parsed_response=parsed_response)
            _handled_data.append(_handled_data_row)
        return _handled_data


    @staticmethod
    def _get_lock_feature(lock: bool = True, sema_value: int = 1) -> Union[LockFactory, BoundedSemaphoreFactory]:
        """
        Initialize Lock or Semaphore. Why? because of persistence process.

        :param lock: It would initial a Lock if it's True, or it would initial Semaphore.
        :param sema_value: The value of Semaphore. This argument only work for option *lock* is False.
        :return: It would return **LockFactory** if option *lock* is True, or it returns **BoundedSemaphoreFactory**.
        """

        if lock is True:
            feature = LockFactory()
        else:
            if sema_value <= 0:
                raise ValueError("The number of Semaphore cannot less than or equal to 0.")
            feature = BoundedSemaphoreFactory(value=sema_value)
        return feature


    @staticmethod
    def _divide_urls(urls: List[str], executor_number: int) -> List[List[str]]:
        """
        Divide the data list which saving URLs to be a list saving multiple lists.

        :param urls: A collection of URLs.
        :param executor_number: How many executors you activate to run.
        :return: A collection of element which also is collection of URLs.
        """

        urls_len = len(urls)
        urls_interval = int(urls_len / executor_number)
        urls_list_collection = [urls[i:i + urls_interval] for i in range(0, executor_number, urls_interval)]
        return urls_list_collection



class AsyncSimpleCrawler(MultiRunnableCrawler):

    def __init__(self, executors: int, factory: AsyncCrawlerFactory = None):
        super(AsyncSimpleCrawler, self).__init__(factory=factory)
        self.__executor_number = executors
        self.__executor = SimpleExecutor(mode=RunningMode.Asynchronous, executors=executors)


    def _initial_factory(self) -> AsyncCrawlerFactory:
        """
        Initial asynchronous version of BaseFactory object --- AsyncCrawlerFactory.

        :return: AsyncCrawlerFactory instance.
        """

        return AsyncCrawlerFactory()


    async def crawl(self, url: str, method: str, retry: int = 1, *args, **kwargs) -> Any:
        response = await self.send_http_request(method=method, url=url, retry=retry, *args, **kwargs)
        parsed_response = await self.parse_http_response(response=response)
        return parsed_response


    async def send_http_request(self, method: str, url: str, retry: int = 1, *args, **kwargs) -> Generic[T]:
        """
        The asynchronous version of *BaseCrawler.send_http_request*.

        :param method: HTTP method.
        :param url: URL.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :return: A HTTP response object.
        """

        response = await self._factory.http_factory.request(method=method, url=url, timeout=retry, *args, **kwargs)
        return response


    async def parse_http_response(self, response: Generic[T]) -> Generic[T]:
        """
        The asynchronous version of *BaseCrawler.parse_http_response*.

        :param response: The HTTP response.
        :return: The result which it has parsed from HTTP response. The data type is Generic[T].
        """

        parsed_response = await self._factory.parser_factory.parse_content(response=response)
        return parsed_response


    async def data_process(self, parsed_response: Generic[T]) -> Generic[T]:
        """
        The asynchronous version of *BaseCrawler.data_process*.

        :param parsed_response: The data which has been parsed from HTTP response object.
        :return: The result of data process. The data type is Generic[T].
        """

        data = await self._factory.data_handling_factory.process(result=parsed_response)
        return data


    async def persist(self, data: Any) -> None:
        """
        The asynchronous version of *BaseCrawler.persist*.

        :param data: The target data to persist. In generally, this is the data which has been parsed and handled.
        :return: None
        """
        await self._factory.persistence_factory.save(data=data)


    async def process_with_list(self, method: str, url: List[str], retry: int = 1, *args, **kwargs) -> Any:
        """
        The asynchronous version of *MultiRunnableCrawler.process_with_list*.

        :param method: HTTP method.
        :param url: A collection of URLs.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :return: A list of result of data process.
        """

        _handled_data = []
        for _target_url in url:
            parsed_response = await self.crawl(method=method, url=_target_url, retry=retry)
            _handled_data_row = await self.data_process(parsed_response=parsed_response)
            _handled_data.append(_handled_data_row)
        return _handled_data


    async def process_with_queue(self, method: str, url: Queue, retry: int = 1, *args, **kwargs) -> Any:
        """
        The asynchronous version of *MultiRunnableCrawler.process_with_queue*.

        :param method: HTTP method.
        :param url: Queue of URLs.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :return: A list of result of data process.
        """

        _handled_data = []
        while url.empty() is False:
            _target_url = await url.get()
            parsed_response = await self.crawl(method=method, url=_target_url, retry=retry)
            _handled_data_row = await self.data_process(parsed_response=parsed_response)
            _handled_data.append(_handled_data_row)
        return _handled_data


    def map(self, method: str, url: List[str], retry: int = 1, lock: bool = True, sema_value: int = 1) -> Optional:
        """
        The asynchronous version of *ExecutorCrawler.map*.

        :param method: HTTP method.
        :param url: A collection of URLs.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :param lock: It would initial a Lock if it's True, or it would initial Semaphore.
        :param sema_value: The value of Semaphore. This argument only work for option *lock* is False.
        :return: The result of data process from parsed HTPP response object.
        """

        feature = MultiRunnableCrawler._get_lock_feature(lock=lock, sema_value=sema_value)
        args_iterator = [{"method": method, "url": _url, "retry": retry} for _url in url]

        self.__executor.map(
            function=self.crawl,
            args_iter=args_iterator,
            queue_tasks=None,
            features=feature)
        result = self.__executor.result()
        return result


    def run(self, method: str, url: Union[List[str], Queue], retry: int = 1, lock: bool = True, sema_value: int = 1) -> Optional:
        """
        The asynchronous version of *ExecutorCrawler.run*.

        :param method: HTTP method.
        :param url: A collection of URLs.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :param lock: It would initial a Lock if it's True, or it would initial Semaphore.
        :param sema_value: The value of Semaphore. This argument only work for option *lock* is False.
        :return: The result of data process from parsed HTPP response object.
        """

        feature = MultiRunnableCrawler._get_lock_feature(lock=lock, sema_value=sema_value)

        if type(url) is list:
            _url_len = len(url)
            if _url_len <= self.__executor_number:
                return self.map(method=method, url=url, retry=retry, lock=lock, sema_value=sema_value)
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



class ExecutorCrawler(MultiRunnableCrawler):

    def __init__(self, mode: RunningMode, executors: int, factory: CrawlerFactory):
        super(ExecutorCrawler, self).__init__(factory=factory)
        self.__executor_number = executors
        self.__executor = SimpleExecutor(mode=mode, executors=executors)


    def run(self, method: str, url: Union[List[str], Queue], retry: int = 1, lock: bool = True, sema_value: int = 1) -> Optional:
        """
        Run the crawl process as multiple executor directly. It may run a little bit differently by the option *url*.
        Please consider below scenarios:

        * Option *url* is a *list* type value:

            * If the size of value is bigger than the executor number:
            separate the collection of URLs and activate the number of executors.

            * If the size of value is smaller than the executor number:
            activate the executors as function *map*.

        * Option *url* is a **Queue** type value:
        Run the executors with the Queue object.

        :param method: HTTP method.
        :param url: A collection of URLs.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :param lock: It would initial a Lock if it's True, or it would initial Semaphore.
        :param sema_value: The value of Semaphore. This argument only work for option *lock* is False.
        :return: The result of data process from parsed HTPP response object.
        """

        feature = MultiRunnableCrawler._get_lock_feature(lock=lock, sema_value=sema_value)

        if type(url) is list:
            urls_len = len(url)
            if urls_len <= self.__executor_number:
                logging.warning("It will have some idle executors deosn't be activated because target URLs amount more than executor number.")
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
        """
        The crawler version of builtin function *map*. It would activate multiple executors as many as the size of
        collection of URLs to run.

        :param method: HTTP method.
        :param url: A collection of URLs.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :param lock: It would initial a Lock if it's True, or it would initial Semaphore.
        :param sema_value: The value of Semaphore. This argument only work for option *lock* is False.
        :return: The result of data process from parsed HTPP response object.
        """

        feature = MultiRunnableCrawler._get_lock_feature(lock=lock, sema_value=sema_value)
        args_iterator = [{"method": method, "url": _url, "retry": retry} for _url in url]

        self.__executor.map(
            function=self.crawl,
            args_iter=args_iterator,
            queue_tasks=None,
            features=feature)
        result = self.__executor.result()
        return result



class PoolCrawler(MultiRunnableCrawler):

    def __init__(self, mode: RunningMode, pool_size: int, factory: CrawlerFactory):
        super(PoolCrawler, self).__init__(factory=factory)
        self.__pool = SimplePool(mode=mode, pool_size=pool_size)


    def __enter__(self):
        self.init()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


    def init(self, lock: bool = True, sema_value: int = 1) -> None:
        """
        Initialize something which be needed before instantiate Pool object.

        :param lock:
        :param sema_value:
        :return:
        """

        feature = MultiRunnableCrawler._get_lock_feature(lock=lock, sema_value=sema_value)
        self.__pool.initial(queue_tasks=None, features=feature)


    def apply(self, method: str, urls: List[str], retry: int = 1) -> Optional:
        """
        Run the crawl process with multiple executor of *Pool*.

        :param method: HTTP method.
        :param urls: A collection of URLs.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :return:
        """

        _urls_len = len(urls)
        _kwargs_iter = [{"method": method, "url": _url, "retry": retry} for _url in urls]
        self.__pool.apply_with_iter(
            functions_iter=[self.crawl for _ in range(_urls_len)],
            kwargs_iter=_kwargs_iter)
        result = self.__pool.get_result()
        return result


    def async_apply(self,
                    method: str, urls: List[str], retry: int = 1,
                    callbacks: Union[Callable, List[Callable]] = None,
                    error_callbacks: Union[Callable, List[Callable]] = None) -> Optional:
        """
        Asynchronous version of *PoolCrawler.apply*.

        :param method: HTTP method.
        :param urls: A collection of URLs.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :param callbacks: A *Callable* type object which would be run after done the task.
        :param error_callbacks: A *Callable* type object which would be run if it gets any exceptions in running.
        :return:
        """

        _urls_len = len(urls)

        _kwargs_iter = [{"method": method, "url": _url, "retry": retry} for _url in urls]

        if callbacks:
            if type(callbacks) is not Iterable:
                callbacks = [callbacks for _ in range(_urls_len)]
            else:
                if len(callbacks) != _urls_len:
                    raise ValueError

        if error_callbacks:
            if type(error_callbacks) is not Iterable:
                error_callbacks = [error_callbacks for _ in range(_urls_len)]
            else:
                if len(callbacks) != _urls_len:
                    raise ValueError

        self.__pool.async_apply_with_iter(
            functions_iter=[self.crawl for _ in range(_urls_len)],
            kwargs_iter=_kwargs_iter,
            callback_iter=callbacks,
            error_callback_iter=error_callbacks)
        result = self.__pool.get_result()
        return result


    def map(self, method: str, urls: List[str], retry: int = 1) -> Optional:
        """
        The *Pool* version of *ExecutorCrawler.map*.

        :param method: HTTP method.
        :param urls: A collection of URLs.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :return:
        """

        _arguments = [(method, _url, retry) for _url in urls]
        self.__pool.map_by_args(function=self.crawl, args_iter=_arguments)
        result = self.__pool.get_result()
        return result


    def async_map(self,
                  method: str, urls: List[str], retry: int = 1,
                  callbacks: Union[Callable, List[Callable]] = None,
                  error_callbacks: Union[Callable, List[Callable]] = None) -> Optional:
        """
        Asynchronous version of *PoolCrawler.map*.

        :param method: HTTP method.
        :param urls: A collection of URLs.
        :param retry: How many it would retry to send HTTP request if it gets fail when sends request.
        :param callbacks: A *Callable* type object which would be run after done the task.
        :param error_callbacks: A *Callable* type object which would be run if it gets any exceptions in running.
        :return:
        """

        _arguments = [(method, _url, retry) for _url in urls]
        self.__pool.async_map_by_args(
            function=self.crawl,
            args_iter=_arguments,
            callback=callbacks,
            error_callback=error_callbacks)
        result = self.__pool.get_result()
        return result


    def terminal(self) -> None:
        """
        Terminate the running of Pool.

        :return: None
        """

        self.__pool.terminal()


    def close(self) -> None:
        """
        Close the resource of the Pool.

        :return: None
        """

        self.__pool.close()

