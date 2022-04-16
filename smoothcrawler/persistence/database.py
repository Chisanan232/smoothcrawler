from multirunnable.persistence.database.strategy import get_connection_pool
from multirunnable.persistence.database import BaseSingleConnection, BaseConnectionPool, DatabaseOperator, BaseDao
from abc import ABC, abstractmethod



class BaseCrawlerSingleConnection(BaseSingleConnection, ABC):
    pass



class BaseCrawlerConnectionPool(BaseConnectionPool, ABC):
    pass



class BaseCrawlerDatabaseOperator(DatabaseOperator, ABC):
    pass



class BaseCrawlerDao(BaseDao, ABC):
    pass

