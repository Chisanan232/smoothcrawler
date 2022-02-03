from smoothcrawler.components.httpio import HTTP, AsyncHTTP
import requests
import urllib3
import aiohttp
import random
import time


_HTTP_Header = {
    "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
                }


class Urllib3HTTPRequest(HTTP):

    __Http_Response = None

    def get(self, url: str, *args, **kwargs):
        _http = urllib3.PoolManager()
        # _random_sleep = random.randrange(0, 10)
        # time.sleep(_random_sleep)
        self.__Http_Response = _http.request("GET", url)
        return self.__Http_Response



class RequestsHTTPRequest(HTTP):

    __Http_Response = None

    def get(self, url: str, *args, **kwargs):
        # _random_sleep = random.randrange(0, 10)
        # time.sleep(_random_sleep)
        self.__Http_Response = requests.get(url, headers=_HTTP_Header)
        return self.__Http_Response



class AsyncHTTPRequest(AsyncHTTP):

    __Http_Response = None

    async def get(self, url: str, *args, **kwargs):
        async with aiohttp.ClientSession() as _async_sess:
            # async with _async_sess.get(url) as _resp:
            #     print(f"[DEBUG] _resp: {_resp}")
            #     # assert _resp.status == 200
            #     # print(f"[DEBUG] _resp.status: {_resp.status}")
            #     # _html = await _resp.read()
            #     _html = await _resp.json()
            #     print(f"[DEBUG] Result HTML: {_html}")
            #     return _html
            #     # return _resp

            _resp = await _async_sess.get(url)
            return _resp

