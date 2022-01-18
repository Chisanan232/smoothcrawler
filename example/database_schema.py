#! /etc/anaconda/python3

from typing import List
from enum import Enum
import re



class TableNameShouldNotBeNone(Exception):

    def __str__(self):
        return "Cannot find target table name."



class KeySpace(Enum):

    TW_Stock: str = "tw_stock"
    US_Stock: str = "us_stock"



class Tables(Enum):

    LIMITED_COMPANY = "limited_company"
    STOCK_DATA = "stock_data"



class Columns:

    __Stock_Data_Table_Name = "stock_data_"

    def schema(self, table_name):
        pass


    @classmethod
    def columns(cls, table_name: Tables) -> List[str]:
        if table_name is Tables.LIMITED_COMPANY:
            return ["stock_symbol", "company", "ISIN", "listed_date", "listed_type", "industry_type", "CFICode"]
        elif table_name is Tables.STOCK_DATA:
            return ["stock_date", "trade_volume", "turnover_price", "opening_price", "highest_price", "lowest_price", "closing_price", "gross_spread", "turnover_volume"]
        elif re.search(re.escape(cls.__Stock_Data_Table_Name), str(table_name)) is not None:
            return ["stock_date", "trade_volume", "turnover_price", "opening_price", "highest_price", "lowest_price", "closing_price", "gross_spread", "turnover_volume"]
        else:
            raise TableNameShouldNotBeNone

