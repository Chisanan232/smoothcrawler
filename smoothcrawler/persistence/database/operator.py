from smoothcrawler.persistence.database.strategy import BaseDatabaseConnection as _BaseDataBaseConnection

from abc import ABCMeta, ABC, abstractmethod
from typing import Tuple, TypeVar, Generic, Any


T = TypeVar("T")


class BaseDatabaseOperator(metaclass=ABCMeta):

    def __init__(self, conn_strategy: _BaseDataBaseConnection):
        self._conn_strategy = conn_strategy


    @abstractmethod
    def initial(self) -> Generic[T]:
        pass


    @property
    @abstractmethod
    def column_names(self) -> Generic[T]:
        pass


    @property
    @abstractmethod
    def row_count(self) -> Generic[T]:
        pass


    @abstractmethod
    def next(self) -> Generic[T]:
        pass


    @abstractmethod
    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> Generic[T]:
        pass


    @abstractmethod
    def execute_many(self, operator: Any, seq_params=None) -> Generic[T]:
        pass


    @abstractmethod
    def fetch(self) -> Generic[T]:
        pass


    @abstractmethod
    def fetch_one(self) -> Generic[T]:
        pass


    @abstractmethod
    def fetch_many(self, size: int = None) -> Generic[T]:
        pass


    @abstractmethod
    def fetch_all(self) -> Generic[T]:
        pass


    @abstractmethod
    def reset(self) -> None:
        pass


    @abstractmethod
    def close(self) -> None:
        pass



class DatabaseOperator(BaseDatabaseOperator, ABC):

    def initial(self, **kwargs) -> None:
        self._conn_strategy.initialize(**kwargs)


    def close(self) -> None:
        self._conn_strategy.close()

