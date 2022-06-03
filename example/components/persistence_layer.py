"""
The Database config:
CREATE DATABASE tw_stock character set utf8;


The database tables schema:

Table <limited_company>:
"stock_symbol", "company", "ISIN", "listed_date", "listed_type", "industry_type", "CFICode"
CREATE TABLE IF NOT EXISTS limited_company (
  stock_symbol VARCHAR(16) NOT NULL,
  company VARCHAR(32) collate utf8_unicode_ci NOT NULL,
  ISIN VARCHAR(16),
  listed_date DATETIME,
  listed_type VARCHAR(16) collate utf8_unicode_ci,
  industry_type VARCHAR(16) collate utf8_unicode_ci,
  CFICode VARCHAR(16),
  PRIMARY KEY(stock_symbol, company)) DEFAULT CHARSET=utf8;

Table <limited_company>:  (not correct)
"date", "trade_volume_share", "turnover", "open_price", "highest_price", "lowest_price", "close_price", "change", "transaction"
CREATE TABLE IF NOT EXISTS stock_data_<corp_stock_symbol> (
  stock_date DATETIME NOT NULL,
  trade_volume DECIMAL(12,4) NOT NULL,
  turnover_price DECIMAL(16,4) NOT NULL,
  opening_price DECIMAL(8,4) NOT NULL,
  highest_price DECIMAL(8,4) NOT NULL,
  lowest_price DECIMAL(8,4) NOT NULL,
  closing_price DECIMAL(8,4) NOT NULL,
  gross_spread DECIMAL(8,4) NOT NULL,
  turnover_volume DECIMAL(12,4) NOT NULL,
  PRIMARY KEY(date)) DEFAULT CHARSET=utf8;

columns:
"日期",
"成交股數",
"成交金額",
"開盤價",
"最高價",
"最低價",
"收盤價",
"漲跌價差",
"成交筆數"

Note:
    Check CMD:
    SHOW VARIABLES LIKE 'character_set_%';    # Verify the character encoding in databases
    SHOW VARIABLES LIKE 'collation_%';

    Modify CMD:
    SET NAMES 'utf8';    ( ==
        SET character_set_client = utf8;
        SET character_set_results = utf8;
        SET character_set_connection = utf8;
    )
    ALTER DATABASE name character set utf8;
    ALTER TABLE type character set utf8;
    ALTER TABLE type modify type_name varchar(50) CHARACTER SET utf8;

"""
from multirunnable.persistence.database.strategy import BaseDatabaseConnection
from multirunnable.persistence.database.layer import BaseDao
from multirunnable.persistence.file.layer import BaseFao

from .mysql_impl import MySQLSingleConnection, MySQLDriverConnectionPool, MySQLOperator

from mysql.connector import errorcode
from mysql.connector.errors import DatabaseError
from typing import List, Tuple, Dict, Union



class StockDao(BaseDao):

    __Stock_Table_Name: str = "stock_data_"
    __Database_Config: Dict[str, str] = {}

    def __init__(self, db_driver: str = None, use_pool: bool = False, **kwargs):
        self._db_driver = db_driver
        self._use_pool = use_pool
        # self.__database_connection = None
        self.__database_opt = None

        # self._database_opts = None
        self._database_config = {
            "host": "127.0.0.1",
            # "host": "172.17.0.6",
            "port": "3306",
            "user": "root",
            "password": "password",
            "database": "tw_stock"
        }

        super().__init__()


    def _instantiate_strategy(self) -> BaseDatabaseConnection:
        if self._db_driver == "mysql":
            # from db_mysql import MySQLSingleConnection, MySQLDriverConnectionPool, MySQLOperator
            if self._use_pool is True:
                db_conn_strategy = MySQLDriverConnectionPool(**self._database_config)
            else:
                db_conn_strategy = MySQLSingleConnection(**self._database_config)
            return db_conn_strategy
        else:
            raise ValueError


    def _instantiate_database_opts(self, strategy: BaseDatabaseConnection) -> MySQLOperator:
        if self.__database_opt is None:
            if self._use_pool is True:
                __database_connection = MySQLDriverConnectionPool(**self._database_config)
            else:
                __database_connection = MySQLSingleConnection(**self._database_config)
            # self.__db_connection = conn_strategy.connection
            self.__database_opt = MySQLOperator(conn_strategy=__database_connection)
        return self.__database_opt


    def set_config(self, **kwargs) -> None:
        self.__Database_Config.update(**kwargs)


    def get_tables(self, database: str) -> List[str]:
        # super(MySQLDB, self).checker(session=self.__session)
        sql = f"SELECT table_name FROM information_schema.tables " \
              f"WHERE table_schema = '{database}';"

        self.execute(sql)
        tables = list(self.fetch_all())
        return [t[0] for t in tables]


    def create_stock_data_table(self, stock_symbol: str) -> bool:
        # super(MySQLDB, self).checker(session=self.__session)
        sql = f"CREATE TABLE IF NOT EXISTS {self.__Stock_Table_Name}{stock_symbol} ( \
                  stock_date DATETIME NOT NULL, \
                  trade_volume NUMERIC(12) NOT NULL, \
                  turnover_price NUMERIC(16) NOT NULL, \
                  opening_price DECIMAL(8,4) NOT NULL, \
                  highest_price DECIMAL(8,4) NOT NULL, \
                  lowest_price DECIMAL(8,4) NOT NULL, \
                  closing_price DECIMAL(8,4) NOT NULL,  \
                  gross_spread VARCHAR(12) NOT NULL, \
                  turnover_volume NUMERIC(12) NOT NULL, \
                  PRIMARY KEY(stock_date)) DEFAULT CHARSET=UTF8MB4"

        try:
            self.execute(sql)
            self.commit()
        except DatabaseError as e:
            if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                return True
            else:
                print(e)
                return False
        except Exception as e:
            print(e)
            return False
        else:
            return True


    def get(self, table: str, columns: str):
        # super(MySQLDB, self).checker(session=self.__session)
        if columns is None:
            columns = "*"
        sql = f"SELECT {columns} FROM {table}"

        ## Method 1
        return self.execute(sql)
        # self.__Database_Cursor.execute(sql)
        ## Method 2
        # return self.__Database_Cursor.fetchall()
        ## Method 3
        # return self.__Database_Cursor.fetchmany(3000)


    def insert(self, data: Union[str, List, Tuple, Dict], table: str, columns: Union[str, List, Tuple, Dict] = None) -> None:
        # super(MySQLDB, self).checker(session=self.__session)

        if type(data) is dict:
            columns = ",".join(data.keys())
            data = ",".join(data.values())

        else:
            if columns is None:
                # columns = self.columns
                raise ValueError("Columns cannot be empty.")

            if type(columns) is not str and type(data) is not str:
                if len(columns) != len(data):
                    raise ValueError("Columns and data doesn't map.")
                    # raise ColumnsAndDataNotBeMapping

                columns = ",".join(columns)
                data = ",".join(data)

        sql = f"INSERT INTO {table} ({columns}) VALUES ({data})"

        self.execute(sql)
        self.commit()


    def batch_insert(self, table: str, columns: List[str], data: List[tuple]) -> None:
        # super(MySQLDB, self).checker(session=self.__session)

        sql_columns = ",".join(columns)
        data_values = ["%s" for _ in range(len(columns))]
        sql_data_values = ", ".join(data_values)

        sql = f"INSERT INTO {table} ({sql_columns}) VALUES ({sql_data_values})"

        self.execute_many(sql, data)
        self.commit()



class StockFao(BaseFao):
    pass

