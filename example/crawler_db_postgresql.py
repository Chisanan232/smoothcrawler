from smoothcrawler.persistence.database.strategy import BaseDatabaseConnection, T
from smoothcrawler.persistence.database import SingleConnection, ConnectionPool, DatabaseOperator

from typing import Generic, Any, Tuple
from psycopg2._psycopg.connection import connection as PostgreSQLConnection
from psycopg2._psycopg.cursor import cursor as PostgreSQLCursor
import psycopg2



class PostgreSQLSingleConnection(SingleConnection):

    @property
    def connection(self) -> PostgreSQLConnection:
        return super(PostgreSQLSingleConnection, self).connection()


    @connection.setter
    def connection(self, conn: PostgreSQLConnection) -> None:
        super(PostgreSQLSingleConnection, self).connection = conn


    @property
    def cursor(self) -> PostgreSQLCursor:
        return super(PostgreSQLSingleConnection, self).cursor()


    @cursor.setter
    def cursor(self, cur: PostgreSQLCursor) -> None:
        super(PostgreSQLSingleConnection, self).cursor = cur


    def connect_database(self, **kwargs) -> PostgreSQLConnection:
        return psycopg2.connect(**self._Database_Config)


    def build_cursor(self) -> PostgreSQLCursor:
        self.cursor = self.connection.cursor()
        return self.cursor


    def commit(self) -> None:
        self.connection.commit()


    def close(self) -> None:
        if self.connection is not None:
            if self.cursor is not None and self.cursor.closed:
                self.cursor.close()
            self.connection.close()



class PostgreSQLDriverConnectionPool(ConnectionPool):

    def connect_database(self, **kwargs) -> Generic[T]:
        pass


    def get_one_connection(self) -> Generic[T]:
        pass


    def build_cursor(self) -> Generic[T]:
        pass


    def commit(self) -> None:
        pass


    def close_pool(self) -> None:
        pass


    def close(self) -> None:
        pass



class PostgreSQLOperator(DatabaseOperator):

    def __init__(self, conn_strategy: BaseDatabaseConnection):
        super(PostgreSQLOperator, self).__init__(conn_strategy=conn_strategy)
        self.__cursor: PostgreSQLCursor = conn_strategy.cursor


    @property
    def row_count(self) -> PostgreSQLCursor:
        return self.__cursor.rowcount


    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> PostgreSQLCursor:
        return self.__cursor.execute(query=operator, vars=params)


    def execute_many(self, operator: Any, seq_params=None) -> PostgreSQLCursor:
        return self.__cursor.executemany(query=operator, vars_list=seq_params)


    def fetch_one(self) -> PostgreSQLCursor:
        return self.__cursor.fetchone()


    def fetch_many(self, size: int = None) -> PostgreSQLCursor:
        return self.__cursor.fetchmany(size=size)


    def fetch_all(self) -> PostgreSQLCursor:
        return self.__cursor.fetchall()

