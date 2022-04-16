from typing import TypeVar, Generic
from abc import ABCMeta, abstractmethod

from .components.httpio import HTTP, AsyncHTTP
from .components.data import (
    BaseHTTPResponseParser, BaseDataHandler,
    BaseAsyncHTTPResponseParser, BaseAsyncDataHandler
)
from .persistence import PersistenceFacade


T = TypeVar("T")


class BaseFactory(metaclass=ABCMeta):

    @property
    @abstractmethod
    def http_factory(self) -> Generic[T]:
        pass


    @property
    @abstractmethod
    def parser_factory(self) -> Generic[T]:
        pass


    @property
    @abstractmethod
    def data_handling_factory(self) -> Generic[T]:
        pass


    @property
    @abstractmethod
    def persistence_factory(self) -> Generic[T]:
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
        self.__http_factory = factory


    @property
    def parser_factory(self) -> BaseHTTPResponseParser:
        return self.__response_parser_factory


    @parser_factory.setter
    def parser_factory(self, factory: BaseHTTPResponseParser) -> None:
        self.__response_parser_factory = factory


    @property
    def data_handling_factory(self) -> BaseDataHandler:
        return self.__data_handling_factory


    @data_handling_factory.setter
    def data_handling_factory(self, factory: BaseDataHandler) -> None:
        self.__data_handling_factory = factory


    @property
    def persistence_factory(self) -> PersistenceFacade:
        return self.__persistence_factory


    @persistence_factory.setter
    def persistence_factory(self, factory: PersistenceFacade) -> None:
        self.__persistence_factory = factory



class AsyncCrawlerFactory(BaseFactory):

    def __init__(self):
        self.__http_factory: AsyncHTTP = None
        self.__response_parser_factory: BaseAsyncHTTPResponseParser = None
        self.__data_handling_factory: BaseAsyncDataHandler = None
        self.__persistence_factory: PersistenceFacade = None


    @property
    def http_factory(self) -> AsyncHTTP:
        return self.__http_factory


    @http_factory.setter
    def http_factory(self, factory: AsyncHTTP) -> None:
        self.__http_factory = factory


    @property
    def parser_factory(self) -> BaseAsyncHTTPResponseParser:
        return self.__response_parser_factory


    @parser_factory.setter
    def parser_factory(self, factory: BaseAsyncHTTPResponseParser) -> None:
        self.__response_parser_factory = factory


    @property
    def data_handling_factory(self) -> BaseAsyncDataHandler:
        return self.__data_handling_factory


    @data_handling_factory.setter
    def data_handling_factory(self, factory: BaseAsyncDataHandler) -> None:
        self.__data_handling_factory = factory


    @property
    def persistence_factory(self) -> PersistenceFacade:
        return self.__persistence_factory


    @persistence_factory.setter
    def persistence_factory(self, factory: PersistenceFacade) -> None:
        self.__persistence_factory = factory

