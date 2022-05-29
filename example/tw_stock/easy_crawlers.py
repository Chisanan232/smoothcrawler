from smoothcrawler.crawler import SimpleCrawler
import urllib3
import json


class TaiwanStockEasyCrawler(SimpleCrawler):

    def send_http_request(self, method: str, url: str, retry: int = 1, *args, **kwargs) -> urllib3.response.HTTPResponse:
        _http = urllib3.PoolManager()
        # _random_sleep = random.randrange(0, 10)
        # time.sleep(_random_sleep)
        _response = _http.request("GET", url)
        return _response


    def parse_http_response(self, response: urllib3.response.HTTPResponse) -> str:
        _data = response.data.decode("utf-8")
        return _data


    def data_process(self, parsed_response: str) -> list:
        print(f"[DEBUG] result: {parsed_response}")
        _result_json = json.loads(parsed_response)
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

