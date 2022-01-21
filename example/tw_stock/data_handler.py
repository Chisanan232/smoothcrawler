from smoothcrawler.components.data import BaseDataHandler, BaseAsyncDataHandler
import json



class StockDataHandler(BaseDataHandler):

    def process(self, result):
        print(f"[DEBUG] result: {result}")
        _result_json = json.loads(result)
        _result_data = _result_json["data"]

        _final_data = []
        _data_row = []

        for _d in _result_data:
            # # stock_date
            _data_row.append(_d[0].replace("/", "-"))
            # # trade_volume
            _data_row.append(int(_d[1].replace(",", "")))
            # # turnover_price
            _data_row.append(int(_d[2].replace(",", "")))
            # # opening_price
            _data_row.append(float(_d[3]))
            # # highest_price
            _data_row.append(float(_d[4]))
            # # lowest_price
            _data_row.append(float(_d[5]))
            # # closing_price
            _data_row.append(float(_d[6]))
            # # gross_spread
            _data_row.append(str(_d[7]))
            # # turnover_volume
            _data_row.append(int(_d[8].replace(",", "")))

            _final_data.append(_data_row.copy())
            _data_row[:] = []

        return _final_data



class StockAsyncDataHandler(BaseAsyncDataHandler):

    async def process(self, result):
        _result_json = json.loads(result)
        _result_data = _result_json["data"]

        _final_data = []
        _data_row = []

        for _d in _result_data:
            # # stock_date
            _data_row.append(_d[0].replace("/", "-"))
            # # trade_volume
            _data_row.append(int(_d[1].replace(",", "")))
            # # turnover_price
            _data_row.append(int(_d[2].replace(",", "")))
            # # opening_price
            _data_row.append(float(_d[3]))
            # # highest_price
            _data_row.append(float(_d[4]))
            # # lowest_price
            _data_row.append(float(_d[5]))
            # # closing_price
            _data_row.append(float(_d[6]))
            # # gross_spread
            _data_row.append(str(_d[7]))
            # # turnover_volume
            _data_row.append(int(_d[8].replace(",", "")))

            _final_data.append(_data_row.copy())
            _data_row[:] = []

        return _final_data


