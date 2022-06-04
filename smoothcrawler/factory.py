from typing import TypeVar, Generic, Any
from abc import ABCMeta, abstractmethod

from .components.persistence import PersistenceFacade
from .components.httpio import HTTP, AsyncHTTP
from .components.data import (
    BaseHTTPResponseParser, BaseDataHandler,
    BaseAsyncHTTPResponseParser, BaseAsyncDataHandler
)


class FactoryTypeError(TypeError):

    def __init__(self, factory: object, factory_type: object):
        self.__factory = factory
        self.__factory_type = factory_type

    def __str__(self):
        return f"The factory object {self.__factory} should extends {self.__factory_type.__class__} and implements its rules functions."


def _chk_factory_type(__factory: object, __class: Any):
    if __factory is not None and isinstance(__factory, __class) is False:
        raise FactoryTypeError(factory=__factory, factory_type=__class)


T = TypeVar("T")


class BaseFactory(metaclass=ABCMeta):

    @property
    @abstractmethod
    def http_factory(self) -> Generic[T]:
        """
        A property for component HTTP sender.

        :return: HTTP sender instance. It should be HTTP or AsyncHTTP type object.
        """
        pass


    @http_factory.setter
    @abstractmethod
    def http_factory(self, factory: Generic[T]) -> None:
        pass


    @property
    @abstractmethod
    def parser_factory(self) -> Generic[T]:
        """
        A property for component HTTP response parser.

        :return: HTTP sender instance. It should be BaseHTTPResponseParser or BaseAsyncHTTPResponseParser type object.
        """
        pass


    @parser_factory.setter
    @abstractmethod
    def parser_factory(self, factory: Generic[T]) -> None:
        pass


    @property
    @abstractmethod
    def data_handling_factory(self) -> Generic[T]:
        """
        A property for component data processing.

        :return: HTTP sender instance. It should be BaseDataHandler or BaseAsyncDataHandler type object.
        """
        pass


    @data_handling_factory.setter
    @abstractmethod
    def data_handling_factory(self, factory: Generic[T]) -> None:
        pass


    @property
    @abstractmethod
    def persistence_factory(self) -> Generic[T]:
        """
        A property for component persistence.

        :return: HTTP sender instance. It should be PersistenceFacade type object.
        """
        pass


    @persistence_factory.setter
    @abstractmethod
    def persistence_factory(self, factory: Generic[T]) -> None:
        pass



class CrawlerFactory(BaseFactory):

    def __init__(self):
        self.__http_factory: HTTP = None
        self.__response_parser_factory: BaseHTTPResponseParser = None
        self.__data_handling_factory: BaseDataHandler = None
        self.__persistence_factory: PersistenceFacade = None


    @property
    def http_factory(self) -> HTTP:
        return self.__http_factory


    @http_factory.setter
    def http_factory(self, factory: HTTP) -> None:
        _chk_factory_type(factory, HTTP)
        self.__http_factory = factory


    @property
    def parser_factory(self) -> BaseHTTPResponseParser:
        return self.__response_parser_factory


    @parser_factory.setter
    def parser_factory(self, factory: BaseHTTPResponseParser) -> None:
        _chk_factory_type(factory, BaseHTTPResponseParser)
        self.__response_parser_factory = factory


    @property
    def data_handling_factory(self) -> BaseDataHandler:
        return self.__data_handling_factory


    @data_handling_factory.setter
    def data_handling_factory(self, factory: BaseDataHandler) -> None:
        _chk_factory_type(factory, BaseDataHandler)
        self.__data_handling_factory = factory


    @property
    def persistence_factory(self) -> PersistenceFacade:
        return self.__persistence_factory


    @persistence_factory.setter
    def persistence_factory(self, factory: PersistenceFacade) -> None:
        _chk_factory_type(factory, PersistenceFacade)
        self.__persistence_factory = factory



class AsyncCrawlerFactory(BaseFactory):

    def __init__(self):
        self.__http_factory: AsyncHTTP = None
        self.__response_parser_factory: BaseAsyncHTTPResponseParser = None
        self.__data_handling_factory: BaseAsyncDataHandler = None
        self.__persistence_factory: PersistenceFacade = None


    @property
    def http_factory(self) -> AsyncHTTP:
        """
        A property for component asynchronous version of HTTP sender.

        :return: HTTP sender instance. It should be HTTP or AsyncHTTP type object.
        """
        return self.__http_factory


    @http_factory.setter
    def http_factory(self, factory: AsyncHTTP) -> None:
        _chk_factory_type(factory, AsyncHTTP)
        self.__http_factory = factory


    @property
    def parser_factory(self) -> BaseAsyncHTTPResponseParser:
        """
        A property for component asynchronous version of HTTP response parser.

        :return: HTTP sender instance. It should be BaseHTTPResponseParser or BaseAsyncHTTPResponseParser type object.
        """
        return self.__response_parser_factory


    @parser_factory.setter
    def parser_factory(self, factory: BaseAsyncHTTPResponseParser) -> None:
        _chk_factory_type(factory, BaseAsyncHTTPResponseParser)
        self.__response_parser_factory = factory


    @property
    def data_handling_factory(self) -> BaseAsyncDataHandler:
        """
        A property for component asynchronous version of data processing.

        :return: HTTP sender instance. It should be BaseDataHandler or BaseAsyncDataHandler type object.
        """
        return self.__data_handling_factory


    @data_handling_factory.setter
    def data_handling_factory(self, factory: BaseAsyncDataHandler) -> None:
        _chk_factory_type(factory, BaseAsyncDataHandler)
        self.__data_handling_factory = factory


    @property
    def persistence_factory(self) -> PersistenceFacade:
        """
        A property for component asynchronous version of persistence.

        :return: HTTP sender instance. It should be PersistenceFacade type object.
        """
        return self.__persistence_factory


    @persistence_factory.setter
    def persistence_factory(self, factory: PersistenceFacade) -> None:
        _chk_factory_type(factory, PersistenceFacade)
        self.__persistence_factory = factory

