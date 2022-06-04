from bs4 import BeautifulSoup
import requests
import urllib3
import json


class ExampleOlderCrawler:

    def main_process(self, url: str, retry: int = 3) -> requests.Response:
        # Implement all things in a function. It even doesn't has retry mechanism.
        try:
            _response = requests.get(url)
        except Exception as e:
            print("Do something handle error.")
        else:
            _bs = BeautifulSoup(_response.text, "html.parser")
            _example_web_title = _bs.find_all("h1")
            _data = _example_web_title[0].text
            return _data



class StockOlderCrawler:

    def main_process(self, url: str):
        _http = urllib3.PoolManager()
        # _random_sleep = random.randrange(0, 10)
        # time.sleep(_random_sleep)
        try:
            _response = _http.request("GET", url)
        except Exception as e:
            print("Do something handle error.")
        else:
            _data = _response.data.decode("utf-8")
            _result_json = json.loads(_data)
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

