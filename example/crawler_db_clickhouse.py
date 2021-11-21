"""
CREATE TABLE ods.stock_2330_p (
  date DateTime64(3),
  trade_volume_share DECIMAL(8,4),
  turnover DECIMAL(8,4),
  open_price DECIMAL(8,4),
  highest_price DECIMAL(8,4),
  lowest_price DECIMAL(8,4),
  close_price DECIMAL(8,4),
  change DECIMAL(8,4),
  transaction DECIMAL(8,4),
  insert_date DateTime64(3) DEFAULT NOW()
)
ENGINE = ReplicatedReplacingMergeTree('/clickhouse/tables/{layer}--{shard}/ods/stock_2330',
'{replica}')
PARTITION BY data_part
ORDER BY (
  date
)


CREATE TABLE ods.stock_2330 (
  date DateTime64(3),
  trade_volume_share DECIMAL(8,4),
  turnover DECIMAL(8,4),
  open_price DECIMAL(8,4),
  highest_price DECIMAL(8,4),
  lowest_price DECIMAL(8,4),
  close_price DECIMAL(8,4),
  change DECIMAL(8,4),
  transaction DECIMAL(8,4),
  insert_date DateTime64(3) DEFAULT NOW()
)
ENGINE = Distributed('dw_table_sharding_rule',
'ods',
'stock_2330_p',
rand(data_part))


"""

from smoothcrawler.persistence.database.strategy import BaseDatabaseConnection, T
from smoothcrawler.persistence.database import SingleConnection, ConnectionPool, DatabaseOperator

from typing import Generic, Any, Tuple
from clickhouse_driver.dbapi.connection import Connection as ClickHouseConnection
from clickhouse_driver.dbapi.cursor import Cursor as ClickHouseCursor
import clickhouse_driver



class ClickHouseSingleConnection(SingleConnection):
    
    @property
    def connection(self) -> ClickHouseConnection:
        return super(ClickHouseSingleConnection, self).connection()


    @connection.setter
    def connection(self, conn: ClickHouseConnection) -> None:
        super(ClickHouseSingleConnection, self).connection = conn


    @property
    def cursor(self) -> ClickHouseCursor:
        return super(ClickHouseSingleConnection, self).cursor()


    @cursor.setter
    def cursor(self, cur: ClickHouseCursor) -> None:
        super(ClickHouseSingleConnection, self).cursor = cur


    def connect_database(self, **kwargs) -> ClickHouseConnection:
        conn = clickhouse_driver.connect()
        return conn


    def build_cursor(self) -> ClickHouseCursor:
        self.cursor = self.connection.cursor()
        return self.cursor


    def commit(self) -> None:
        self.connection.commit()


    def close(self) -> None:
        if self.connection.is_closed is False:
            if self.cursor is not None:
                self.cursor.close()
            self.connection.close()



class ClickHouseDriverConnectionPool(ConnectionPool):

    def close_pool(self) -> None:
        pass


    def connect_database(self, **kwargs) -> Generic[T]:
        pass


    def get_one_connection(self) -> Generic[T]:
        pass


    def build_cursor(self) -> Generic[T]:
        pass


    def commit(self) -> None:
        pass


    def close(self) -> None:
        pass



class ClickHouseOperator(DatabaseOperator):

    def __init__(self, conn_strategy: BaseDatabaseConnection):
        super(ClickHouseOperator, self).__init__(conn_strategy=conn_strategy)
        self.__cursor: ClickHouseCursor = conn_strategy.cursor


    @property
    def column_names(self) -> ClickHouseCursor:
        return self.__cursor.columns_with_types


    @property
    def row_count(self) -> ClickHouseCursor:
        return self.__cursor.rowcount


    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> ClickHouseCursor:
        return self.__cursor.execute(operation=operator, parameters=params)


    def execute_many(self, operator: Any, seq_params=None) -> ClickHouseCursor:
        return self.__cursor.executemany(operation=operator, seq_of_parameters=seq_params)


    def fetch_one(self) -> ClickHouseCursor:
        return self.__cursor.fetchone()


    def fetch_many(self, size: int = None) -> ClickHouseCursor:
        return self.__cursor.fetchmany(size=size)


    def fetch_all(self) -> ClickHouseCursor:
        return self.__cursor.fetchall()

