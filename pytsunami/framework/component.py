from abc import ABCMeta, abstractmethod
from typing import List, Any
from requests import Response



class BaseComponent(metaclass=ABCMeta):

    pass



class BaseUrlHandler(BaseComponent):

    @abstractmethod
    def url(self):
        pass



class BaseHttpSender(BaseComponent):

    @abstractmethod
    def send(self) -> Response:
        pass


    @abstractmethod
    def retry(self):
        pass



class BaseResponseParser(BaseComponent):

    @abstractmethod
    def parse(self, response: Response) -> List:
        pass



class BaseDataHandler(BaseComponent):

    @abstractmethod
    def data_handling(self, data: List) -> List:
        pass



class BasePersistence(BaseComponent):

    @abstractmethod
    def save(self, data: List) -> None:
        pass

