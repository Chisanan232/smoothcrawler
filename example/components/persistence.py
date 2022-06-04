from multirunnable import set_mode, RunningMode
from multirunnable.persistence.file import SavingStrategy
from smoothcrawler.components.persistence import PersistenceFacade

from .persistence_layer import StockDao, StockFao
from .database_schema import Tables, Columns


_database_config = {
    "host": "127.0.0.1",
    # "host": "172.17.0.6",
    "port": "3306",
    "user": "root",
    "password": "password",
    "database": "tw_stock"
}


class StockDataPersistenceLayer(PersistenceFacade):

    def save(self, data, *args, **kwargs) -> None:
        set_mode(mode=RunningMode.Concurrent)

        _stock_fao = StockFao(strategy=SavingStrategy.ONE_THREAD_ONE_FILE)
        _stock_fao.save_as_csv(file="/Users/bryantliu/Downloads/stock_crawler_2330.csv", mode="a+", data=data)

        _stock_dao = StockDao(db_driver="mysql", **_database_config)
        _stock_dao.create_stock_data_table(stock_symbol="2330")
        _data_rows = [tuple(d) for d in data]
        _stock_dao.batch_insert(table="tw_stock.stock_data_2330", columns=Columns.columns(table_name=Tables.STOCK_DATA), data=_data_rows)

