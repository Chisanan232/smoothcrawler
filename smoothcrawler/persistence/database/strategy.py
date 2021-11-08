from smoothcrawler.persistence.interface import BasePersistence
from smoothcrawler.persistence.configuration import BaseDatabaseConfiguration
from smoothcrawler.persistence.database.configuration import ConfigKey, DefaultConfig
from smoothcrawler.exceptions import GlobalizeObjectError
from smoothcrawler._utils import get_cls_name as _get_cls_name

from abc import ABC, abstractmethod
from typing import Dict, cast, Union
from multirunnable.api import retry, async_retry
from multiprocessing import cpu_count



class BaseDatabaseConnection(BasePersistence):

    _Database_Config: Dict[str, Union[str, int]] = {
        "host": "",
        "port": "",
        "user": "",
        "password": "",
        "database": ""
    }

    _Database_Connection = None
    _Database_Cursor = None

    def __init__(self, **kwargs):
        if kwargs:
            __host_val = kwargs.get("host")
            __port_val = kwargs.get("port")
            __username_val = kwargs.get("user")
            __password_val = kwargs.get("password")
            __database_val = kwargs.get("database")
        else:
            __host_val = DefaultConfig.HOST.value
            __port_val = DefaultConfig.PORT.value
            __username_val = DefaultConfig.USERNAME.value
            __password_val = DefaultConfig.PASSWORD.value
            __database_val = DefaultConfig.DATABASE.value

        self._Database_Config[ConfigKey.USERNAME.value] = __username_val
        self._Database_Config[ConfigKey.PASSWORD.value] = __password_val
        self._Database_Config[ConfigKey.HOST.value] = __host_val
        self._Database_Config[ConfigKey.PORT.value] = __port_val
        self._Database_Config[ConfigKey.DATABASE.value] = __database_val


    def __str__(self):
        __instance_brief = None
        # # self.__class__ value: <class '__main__.ACls'>
        __cls_str = str(self.__class__)
        __cls_name = _get_cls_name(cls_str=__cls_str)
        if __cls_name != "":
            __instance_brief = f"{__cls_name}(configuration={self._Database_Config})"
        else:
            __instance_brief = __cls_str
        return __instance_brief


    def __repr__(self):
        return f"{self.__str__()} at {id(self.__class__)}"


    @property
    def database_config(self) -> Dict[str, object]:
        """
        Description:
            Get all database configuration content.
        :return:
        """
        return self._Database_Config


    @property
    def connection(self) -> object:
        return self._Database_Connection


    @connection.setter
    def connection(self, conn) -> None:
        self._Database_Connection = conn


    @property
    def cursor(self) -> object:
        return self._Database_Cursor


    @cursor.setter
    def cursor(self, cur) -> None:
        self._Database_Cursor = cur


    @abstractmethod
    def initialize(self, **kwargs) -> None:
        """
        Description:
            Initialize something which be needed before operate something with database.
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def connect_database(self, **kwargs) -> object:
        """
        Description:
            Connection to database and return the connection or connection pool instance.
        :return:
        """
        pass


    @abstractmethod
    def get_one_connection(self) -> object:
        """
        Description:
            Get one database connection instance.
        :return:
        """
        pass


    @abstractmethod
    def build_cursor(self) -> object:
        """
        Description:
            Build cursor instance of one specific connection instance.
        :return:
        """
        pass


    @abstractmethod
    def close(self) -> None:
        """
        Description:
            Close connection and cursor instance.
        :return:
        """
        pass


Database_Connection: object = None
Database_Cursor: object = None


class SingleConnection(BaseDatabaseConnection, ABC):

    def __init__(self, **kwargs):
        super(SingleConnection, self).__init__(**kwargs)
        self.initialize(**self._Database_Config)


    def initialize(self, **kwargs) -> None:
        """
        Note:
            Deprecated the method about multiprocessing saving with one connection and change to use multiprocessing
            saving with pool size is 1 connection pool. The reason is database instance of connection pool is already,
            but for the locking situation, we should:
            lock acquire -> new instance -> execute something -> close instance -> lock release . and loop and loop until task finish.
            But connection pool would:
            new connection instances and save to pool -> semaphore acquire -> GET instance (not NEW) ->
            execute something -> release instance back to pool (not CLOSE instance) -> semaphore release

            Because only one connection instance, the every process take turns to using it to saving data. In other words,
            here doesn't need to initial anything about database connection.
        :param kwargs:
        :return:
        """
        self.connection = self.connect_database(**kwargs)
        self.cursor = self.build_cursor()


    def get_one_connection(self) -> object:
        if self.connection is not None:
            return self.connection
        self.connection = self.connect_database()
        return self.connection


Database_Connection_Pool: object = None


class ConnectionPool(BaseDatabaseConnection):

    __Connection_Pool_Name: str = "smoothcrawler"
    _Connection_Pool = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pool_name_val = cast(str, kwargs.get("pool_name", self.__Connection_Pool_Name))
        pool_size_val = cast(int, kwargs.get("pool_size", cpu_count()))

        self._Database_Config["pool_name"] = pool_name_val
        self._Database_Config["pool_size"] = pool_size_val

        self.initialize(**self._Database_Config)


    def initialize(self, **kwargs) -> None:
        """
        Description:
            Target to initialize Process Semaphore and Database connection
            pool object, and globalize them to let processes to use.
        :param kwargs:
        :return:
        """
        # # Database Connections Pool part
        # Initialize the Database Connection Instances Pool.
        self._Connection_Pool = self.connect_database()
        # Globalize object to share between different multiple processes
        Globalize.connection_pool(pool=self._Connection_Pool)


    @property
    def database_connection_pool(self) -> object:
        """
        Description:
            Get the database connection pool which has been globalized.
        :return:
        """
        return Database_Connection_Pool


    @property
    def pool_size(self) -> int:
        """
        Description:
            Set the database connection pool size.
        :return:
        """
        return self._Database_Config["pool_size"]


    @pool_size.setter
    def pool_size(self, pool_size: int) -> None:
        """
        Description:
            Set the database connection pool size.
        :return:
        """
        self._Database_Config["pool_size"] = pool_size


    @abstractmethod
    def close_pool(self) -> None:
        """
        Description:
            Close the database connection pool instance.
        :return:
        """
        pass



class Globalize:

    @staticmethod
    def connection(conn) -> None:
        if conn is not None:
            global Database_Connection
            Database_Connection = conn
        else:
            raise GlobalizeObjectError


    @staticmethod
    def cursor(cursor) -> None:
        if cursor is not None:
            global Database_Cursor
            Database_Cursor = cursor
        else:
            raise GlobalizeObjectError


    @staticmethod
    def connection_pool(pool) -> None:
        if pool is not None:
            global Database_Connection_Pool
            Database_Connection_Pool = pool
        else:
            raise GlobalizeObjectError

