from multirunnable.persistence.database.operator import T
from smoothcrawler.persistence.database import get_connection_pool, BaseCrawlerSingleConnection, BaseCrawlerConnectionPool, BaseCrawlerDatabaseOperator, BaseCrawlerDao

from typing import Any, Tuple, cast, Union, Generic
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from mysql.connector.errors import PoolError
from mysql.connector.cursor import MySQLCursor
import mysql.connector
import logging
import time
import os



class MySQLSingleConnection(BaseCrawlerSingleConnection):

    @property
    def connection(self) -> MySQLConnection:
        return self._database_connection


    def connect_database(self, **kwargs) -> MySQLConnection:
        return mysql.connector.connect(**kwargs)


    def commit(self) -> None:
        self.connection.commit()


    def close(self) -> None:
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            logging.info(f"MySQL connection is closed. - PID: {os.getpid()}")
        else:
            logging.info("Connection has been disconnect or be killed before.")



class MySQLDriverConnectionPool(BaseCrawlerConnectionPool):

    def connect_database(self, **kwargs) -> MySQLConnectionPool:
        connection_pool = MySQLConnectionPool(**kwargs)
        return connection_pool


    def get_one_connection(self, pool_name: str = "", **kwargs) -> PooledMySQLConnection:
        while True:
            try:
                __connection = get_connection_pool(pool_name=pool_name).get_connection()
                logging.info(f"Get a valid connection: {__connection}")
                return __connection
            except PoolError as e:
                logging.error(f"Will sleep for 5 seconds to wait for connection is available. - {self.getName()}")
                time.sleep(5)


    def commit(self) -> None:
        self.connection.commit()


    def close_pool(self, pool_name: str) -> None:
        get_connection_pool(pool_name=pool_name).close()


    def close(self) -> None:
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            logging.info(f"MySQL connection is closed. - PID: {os.getpid()}")
        else:
            logging.info("Connection has been disconnect or be killed before.")



class MySQLOperator(BaseCrawlerDatabaseOperator):

    def __init__(self, conn_strategy: Union[BaseCrawlerSingleConnection, BaseCrawlerConnectionPool], db_config={}):
        super(MySQLOperator, self).__init__(conn_strategy=conn_strategy, db_config=db_config)


    def initial_cursor(self, connection: Union[MySQLConnection, PooledMySQLConnection]) -> MySQLCursor:
        return connection.cursor(buffered=True)


    @property
    def column_names(self) -> MySQLCursor:
        return self._cursor.column_names


    @property
    def row_count(self) -> MySQLCursor:
        return self._cursor.rowcount


    def next(self) -> MySQLCursor:
        return self._cursor.next()


    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> MySQLCursor:
        return self._cursor.execute(operation=operator, params=params, multi=multi)


    def execute_many(self, operator: Any, seq_params=None) -> MySQLCursor:
        return self._cursor.executemany(operation=operator, seq_params=seq_params)


    def fetch(self) -> MySQLCursor:
        return self._cursor.fetch()


    def fetch_one(self) -> MySQLCursor:
        return self._cursor.fetchone()


    def fetch_many(self, size: int = None) -> MySQLCursor:
        return self._cursor.fetchmany(size=size)


    def fetch_all(self) -> MySQLCursor:
        return self._cursor.fetch_all()


    def reset(self) -> None:
        self._cursor.reset()


