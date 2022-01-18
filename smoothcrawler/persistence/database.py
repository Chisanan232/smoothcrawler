from abc import ABC, abstractmethod
from multirunnable.persistence.database import BaseSingleConnection, BaseConnectionPool, DatabaseOperator, BaseDao
from multirunnable.persistence.database.strategy import get_connection_pool



class BaseCrawlerSingleConnection(BaseSingleConnection, ABC):
    pass



class BaseCrawlerConnectionPool(BaseConnectionPool, ABC):
    pass



class BaseCrawlerDatabaseOperator(DatabaseOperator, ABC):
    pass



class BaseCrawlerDao(BaseDao, ABC):
    pass

