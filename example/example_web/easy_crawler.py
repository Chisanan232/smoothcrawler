from smoothcrawler.crawler import SimpleCrawler
from bs4 import BeautifulSoup
import requests


_HTTP_Header = {
    "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
                }


class ExampleEasyCrawler(SimpleCrawler):

    def send_http_request(self, method: str, url: str, retry: int = 1, *args, **kwargs) -> requests.Response:
        _response = requests.get(url, headers=_HTTP_Header)
        return _response


    def parse_http_response(self, response: requests.Response) -> str:
        _bs = BeautifulSoup(response.text, "html.parser")
        _example_web_title = _bs.find_all("h1")
        return _example_web_title[0].text


    def data_process(self, parsed_response: str) -> str:
        return parsed_response

