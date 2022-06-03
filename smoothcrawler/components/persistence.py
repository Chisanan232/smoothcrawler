from abc import ABCMeta, ABC, abstractmethod
from typing import Union, TypeVar, Generic, Iterable, Any


T = TypeVar("T")


class PersistenceFacade(metaclass=ABCMeta):

    @abstractmethod
    def save(self, data: Union[Iterable, Any], *args, **kwargs) -> Generic[T]:
        pass



class BaseCrawlerFao(PersistenceFacade, ABC):

    __File = None

    def save(self, data, file: str = "", mode: str = "a+", encoding: str = "utf-8") -> None:
        self.__File.file_path = file
        self.__File.mode = mode
        self.__File.encoding = encoding

        self.__File.open()
        self.__File.write(data=data)
        self.__File.close()

