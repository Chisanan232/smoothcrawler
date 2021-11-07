from smoothcrawler.persistence.database.strategy import (
    BaseDataBaseConnection as _BaseDataBaseConnection,
    SingleConnection, ConnectionPool)
from smoothcrawler.persistence.database.operator import DatabaseOperator

from typing import Type, Any, Tuple


class DatabaseFacade:

    def __init__(self, strategy: _BaseDataBaseConnection, operator: Type[DatabaseOperator]):
        super(DatabaseFacade, self).__init__()
        self.__db_opt = operator(conn_strategy=strategy)


    @property
    def column_names(self) -> object:
        pass


    @property
    def row_count(self) -> object:
        pass


    def next(self) -> object:
        pass


    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> object:
        pass


    def execute_many(self, operator: Any, seq_params=None) -> object:
        pass


    def fetch(self) -> object:
        pass


    def fetch_one(self) -> object:
        pass


    def fetch_many(self, size: int = None) -> object:
        pass


    def fetch_all(self) -> object:
        pass


    def reset(self) -> None:
        pass

