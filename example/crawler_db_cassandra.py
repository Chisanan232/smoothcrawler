from smoothcrawler.persistence.database.strategy import BaseDatabaseConnection, T
from smoothcrawler.persistence.database import SingleConnection, ConnectionPool, DatabaseOperator

from typing import Generic, Any, Tuple
from cassandra.cluster import Cluster as CassandraCluster, Session as CassandraSession
from cassandra.query import PreparedStatement, SimpleStatement



class CassandraSingleConnection(SingleConnection):

    @property
    def connection(self) -> CassandraCluster:
        return super(CassandraSingleConnection, self).connection


    @property
    def cursor(self) -> CassandraSession:
        return super(CassandraSingleConnection, self).cursor()


    def connect_database(self, **kwargs) -> CassandraCluster:
        cluster = CassandraCluster()
        return cluster


    def build_cursor(self) -> CassandraSession:
        session = self.connection.connect()
        return session


    def commit(self) -> None:
        pass


    def close(self) -> None:
        if self.connection.is_shutdown is False:
            if self.cursor.is_shutdown is False:
                self.cursor.shutdown()
            self.connection.shutdown()



class CassandraDriverConnectionPool(ConnectionPool):

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



class CassandraOperator(DatabaseOperator):

    def __init__(self, conn_strategy: BaseDatabaseConnection):
        super(CassandraOperator, self).__init__(conn_strategy=conn_strategy)
        self.__session: CassandraSession = conn_strategy.cursor


    @property
    def column_names(self) -> Generic[T]:
        pass


    @property
    def row_count(self) -> Generic[T]:
        pass


    def next(self) -> Generic[T]:
        pass


    def execute(self, operator: Any, params: Tuple = None, multi: bool = False) -> Generic[T]:
        self.__session.execute()


    def execute_many(self, operator: Any, seq_params=None) -> Generic[T]:
        pass


    def fetch(self) -> Generic[T]:
        pass


    def fetch_one(self) -> Generic[T]:
        pass


    def fetch_many(self, size: int = None, **kwargs) -> Generic[T]:
        keyspace = kwargs.get("keyspace", "")
        query = kwargs.get("query", None)
        if query is None:
            raise ValueError("SQL query cannot be empty.")
        simple_statement = SimpleStatement(keyspace=keyspace, query_string=query, fetch_size=size)
        yield self.__session.execute(query=simple_statement)


    def fetch_all(self) -> Generic[T]:
        pass


    def reset(self) -> None:
        pass

