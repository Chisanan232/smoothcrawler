from pytsunami.framework.component import BaseHttpSender, BaseResponseParser, BaseDataHandler, BasePersistence

from abc import ABCMeta, abstractmethod



class BaseFactory(metaclass=ABCMeta):

    pass



class BaseCrawlerFactory(BaseFactory):

    @abstractmethod
    def http_sender(self) -> BaseHttpSender:
        pass


    @abstractmethod
    def parser(self) -> BaseResponseParser:
        pass


    @abstractmethod
    def data_handler(self) -> BaseDataHandler:
        pass


    @abstractmethod
    def persistence(self) -> BasePersistence:
        pass

