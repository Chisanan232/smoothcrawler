from smoothcrawler.persistence.database.strategy import BaseDatabaseConnection
from smoothcrawler.persistence.database import SingleConnection, ConnectionPool, DatabaseOperator

from typing import Any, Tuple, cast
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from mysql.connector.errors import PoolError
from mysql.connector.cursor import MySQLCursor
import mysql.connector
import logging
import time
import os



class MySQLSingleConnection(SingleConnection):

    @property
    def connection(self) -> MySQLConnection:
        return super(MySQLSingleConnection, self).connection


    # @connection.setter
    # def connection(self, conn: MySQLConnection) -> None:
    #     super(MySQLSingleConnection, self).connection = conn
    #
    #
    # @property
    # def cursor(self) -> MySQLCursor:
    #     return super(MySQLSingleConnection, self).cursor
    #
    #
    # @cursor.setter
    # def cursor(self, cur: MySQLCursor) -> None:
    #     super(MySQLSingleConnection, self).cursor = cur


    def connect_database(self, **kwargs) -> MySQLConnection:
        return mysql.connector.connect(**self._Database_Config)


    def build_cursor(self) -> MySQLCursor:
        self.cursor = self.connection.cursor()
        return self.cursor


    def commit(self) -> None:
        self.connection.commit()


    def close(self) -> None:
        if self.connection is not None and self.connection.is_connected():
            if self.cursor is not None:
                self.cursor.close()
            self.connection.close()
            logging.info(f"MySQL connection is closed. - PID: {os.getpid()}")
        else:
            logging.info("Connection has been disconnect or be killed before.")



class MySQLDriverConnectionPool(ConnectionPool):

    @property
    def database_connection_pool(self) -> MySQLConnectionPool:
        return super(MySQLDriverConnectionPool, self).database_connection_pool()


    @property
    def connection(self) -> PooledMySQLConnection:
        return super(MySQLDriverConnectionPool, self).connection


    @connection.setter
    def connection(self, conn: PooledMySQLConnection) -> None:
        super(MySQLDriverConnectionPool, self).connection = conn


    @property
    def cursor(self) -> MySQLCursor:
        return super(MySQLDriverConnectionPool, self).cursor


    @cursor.setter
    def cursor(self, cur: MySQLCursor) -> None:
        super(MySQLDriverConnectionPool, self).cursor = cur


    def connect_database(self, **kwargs) -> MySQLConnectionPool:
        connection_pool = MySQLConnectionPool(**self._Database_Config)
        return connection_pool


    def get_one_connection(self) -> PooledMySQLConnection:
        while True:
            try:
                # return self.database_connection_pool.get_connection()
                __connection = self.database_connection_pool.get_connection()
                logging.info(f"Get a valid connection: {__connection}")
                return __connection
            except PoolError as e:
                logging.error(f"Connection Pool: {self.database_connection_pool.pool_size} ")
                logging.error(f"Will sleep for 5 seconds to wait for connection is available. - {self.getName()}")
                time.sleep(5)


    def build_cursor(self) -> MySQLCursor:
        self.cursor = self.connection.cursor()
        return self.cursor


    def commit(self) -> None:
        self.connection.commit()


    def close_pool(self) -> None:
        self.database_connection_pool.close()


    def close(self) -> None:
        if self.connection is not None and self.connection.is_connected():
            if self.cursor is not None:
                self.cursor.close()
            self.connection.close()
            logging.info(f"MySQL connection is closed. - PID: {os.getpid()}")
        else:
            logging.info("Connection has been disconnect or be killed before.")



class MySQLOperator(DatabaseOperator):
    
    def __init__(self, conn_strategy: BaseDatabaseConnection):
        super(MySQLOperator, self).__init__(conn_strategy=conn_strategy)
        self.__cursor: MySQLCursor = conn_strategy.cursor


    @property
    def column_names(self) -> MySQLCursor:
        return self.__cursor.column_names


    @property
    def row_count(self) -> MySQLCursor:
        return self.__cursor.rowcount


    def next(self) -> MySQLCursor:
        return self.__cursor.next()


    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> MySQLCursor:
        return self.__cursor.execute(operation=operator, params=params, multi=multi)


    def execute_many(self, operator: Any, seq_params=None) -> MySQLCursor:
        return self.__cursor.executemany(operation=operator, seq_params=seq_params)


    def fetch(self) -> MySQLCursor:
        return self.__cursor.fetch()


    def fetch_one(self) -> MySQLCursor:
        return self.__cursor.fetchone()


    def fetch_many(self, size: int = None) -> MySQLCursor:
        return self.__cursor.fetchmany(size=size)


    def fetch_all(self) -> MySQLCursor:
        return self.__cursor.fetch_all()


    def reset(self) -> None:
        self.__cursor.reset()


