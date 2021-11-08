from smoothcrawler.persistence.database.strategy import BaseDatabaseConnection as _BaseDataBaseConnection

from abc import ABCMeta, abstractmethod, ABC
from typing import Tuple, Any



class BaseDatabaseOperator(metaclass=ABCMeta):

    def __init__(self, conn_strategy: _BaseDataBaseConnection):
        self._conn_strategy = conn_strategy


    @abstractmethod
    def initial(self) -> object:
        pass


    @property
    @abstractmethod
    def column_names(self) -> object:
        pass


    @property
    @abstractmethod
    def row_count(self) -> object:
        pass


    @abstractmethod
    def next(self) -> object:
        pass


    @abstractmethod
    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> object:
        pass


    @abstractmethod
    def execute_many(self, operator: Any, seq_params=None) -> object:
        pass


    @abstractmethod
    def fetch(self) -> object:
        pass


    @abstractmethod
    def fetch_one(self) -> object:
        pass


    @abstractmethod
    def fetch_many(self, size: int = None) -> object:
        pass


    @abstractmethod
    def fetch_all(self) -> object:
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

