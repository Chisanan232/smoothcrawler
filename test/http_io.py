from smoothcrawler.http_io import BaseHttpIo
from abc import ABCMeta, abstractmethod
import urllib3
import pytest
import http
import time


HTTP_METHOD = "GET"
TEST_URL = "https://www.google.com"
TEST_TIMEOUT_URL = "https://www.test.com"

RETRY_TIMES = 3
REQUEST_TIMEOUT = 5


class BaseHttpTestSpec(metaclass=ABCMeta):

    @abstractmethod
    def request(self, *args, **kwargs):
        pass



class TestHttpRequest(BaseHttpTestSpec):

    """
    Test case:
        Test for sending HTTP request generally.
    """

    class TestRequestsHttpIo(BaseHttpIo):
        __Http_Response = None

        def requests(self, *args, **kwargs):
            http = urllib3.PoolManager()
            self.__Http_Response = http.request(HTTP_METHOD, TEST_URL)
            return self.__Http_Response

        @property
        def status_code(self):
            return self.__Http_Response.status


    def request(self, *args, **kwargs):
        http_cls = self.TestRequestsHttpIo()
        response = http_cls.requests()
        assert response is not None, "It doesn't implement the code which has responsibility about sending HTTP request."
        assert http_cls.status_code is not None, "HTTP status code must to be a value."

        status_code = int(http_cls.status_code)
        assert TestHttpRequest.__status_code_is_valid(status_code) is True, "This is not a valid status code."


    @staticmethod
    def __status_code_is_valid(status):
        for _status in http.HTTPStatus:
            if int(status) == _status.value:
                return True
        else:
            return False


Test_Sleep_Time = REQUEST_TIMEOUT + RETRY_TIMES - 1

Initial_Flag = 0
Done_Flag = 0
Exception_Flag = 0


class _TestRequestsHttpIo(BaseHttpIo):

    __Http_Response = None

    def get(self, *args, **kwargs):
        _http = urllib3.PoolManager()
        global Test_Sleep_Time
        time.sleep(Test_Sleep_Time)
        Test_Sleep_Time -= 1
        self.__Http_Response = _http.request("GET", TEST_URL)
        return self.__Http_Response

    @property
    def status_code(self):
        return self.__Http_Response.status

    def initial(self):
        global Initial_Flag
        Initial_Flag += 1
        print("Initial process.")

    def done_handler(self, result):
        global Done_Flag
        Done_Flag += 1
        print("Task done! ")

    def exception_handler(self, error):
        global Exception_Flag
        Exception_Flag += 1
        print("Got failure when run task.")

    def http_200_response(self, response):
        print("Get the HTTP response successfully.")



class TestRetryHttpGet(BaseHttpTestSpec):

    """
    Test case:
        Test for sending HTTP request with some configuration.
        Setting:
            Timeout feature.
            Retry mechanism.
            HTTP 200 response handler.
    """

    def request(self, *args, **kwargs):
        http_cls = _TestRequestsHttpIo()
        # It will raise TimeoutError if it doesn't get response after 5 seconds later.
        # And it will retry to send HTTP request if it got any exception util overrate the retry times.
        response = http_cls.requests(timeout=REQUEST_TIMEOUT, retry=RETRY_TIMES)
        assert response is not None, "It doesn't implement the code which has responsibility about sending HTTP request."
        assert http_cls.status_code is not None, "HTTP status code must to be a value."

        status_code = int(http_cls.status_code)
        assert TestRetryHttpGet.__status_code_is_valid(status_code) is True, "This is not a valid status code."

        assert Initial_Flag == RETRY_TIMES, ""
        assert Done_Flag == RETRY_TIMES, ""
        assert Exception_Flag == RETRY_TIMES, ""


    @staticmethod
    def __status_code_is_valid(status):
        for _status in http.HTTPStatus:
            if int(status) == _status.value:
                return True
        else:
            return False

