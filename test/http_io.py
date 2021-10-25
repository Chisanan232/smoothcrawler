from smoothcrawler.http_io import BaseHTTP, HTTP, AsyncHTTP, set_retry
from abc import ABCMeta, abstractmethod
import urllib3
import pytest
import http
import time

# Import package multirunnable
import pathlib
import sys
import os

package_multirunnable_path = str(pathlib.Path(__file__).absolute().parent.parent.parent)
final_path = os.path.join(package_multirunnable_path, "apache-multirunnable")
sys.path.append(final_path)

from multirunnable.api import retry


HTTP_METHOD = "GET"
# TEST_URL = "https://www.google.com"
TEST_URL = "https://www.youtube.com"
TEST_TIMEOUT_URL = "https://www.test.com"

RETRY_TIMES = 3
REQUEST_TIMEOUT = 5


class BaseHttpTestSpec(metaclass=ABCMeta):

    @abstractmethod
    def test_request(self, *args, **kwargs):
        pass



class _TestRequestsHTTP(HTTP):

    __Http_Response = None

    def request(self, *args, **kwargs):
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request(HTTP_METHOD, TEST_URL)
        return self.__Http_Response


    @property
    def status_code(self):
        if self.__Http_Response:
            return self.__Http_Response.status
        else:
            return 404



class _TestMethodsHTTP(HTTP):
    __Http_Response = None

    def get(self, *args, **kwargs):
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("GET", TEST_URL)
        return self.__Http_Response


    def post(self, *args, **kwargs):
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("POST", TEST_URL)
        return self.__Http_Response


    def put(self, *args, **kwargs):
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("PUT", TEST_URL)
        return self.__Http_Response


    def delete(self, *args, **kwargs):
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("DELETE", TEST_URL)
        return self.__Http_Response


    def head(self, *args, **kwargs):
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("HEAD", TEST_URL)
        return self.__Http_Response


    def option(self, *args, **kwargs):
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("OPTION", TEST_URL)
        return self.__Http_Response


    @property
    def status_code(self):
        if self.__Http_Response:
            return self.__Http_Response.status
        else:
            return 404



class TestHttpRequest(BaseHttpTestSpec):

    """
    Test case:
        Test for sending HTTP request generally.
    """

    def test_request(self, *args, **kwargs):
        req_ver_http = _TestRequestsHTTP()
        req_response = req_ver_http.request()
        assert req_response is not None, "It doesn't implement the code which has responsibility about sending HTTP request."
        assert req_ver_http.status_code is not None, "HTTP status code must to be a value."

        status_code = int(req_ver_http.status_code)
        assert TestHttpRequest.__status_code_is_valid(status_code) is True, "This is not a valid status code."

        methods_http = _TestMethodsHTTP()
        # Test HTTP method 'GET'
        method_response = methods_http.request(method="GET")
        assert method_response is not None, "It doesn't implement the code which has responsibility about sending HTTP request."
        assert methods_http.status_code is not None, "HTTP status code must to be a value."

        status_code = int(methods_http.status_code)
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
Final_Flag = 0
Exception_Flag = 0


class _TestRetryRequestsHTTP(HTTP):

    __Http_Response = None

    def get(self, *args, **kwargs):
        _http = urllib3.PoolManager()
        global Test_Sleep_Time
        # time.sleep(Test_Sleep_Time)
        if Test_Sleep_Time >= REQUEST_TIMEOUT:
            raise TimeoutError("For testing")
        Test_Sleep_Time -= 1
        self.__Http_Response = _http.request("GET", TEST_URL)
        return self.__Http_Response

    @property
    def status_code(self):
        if self.__Http_Response:
            return self.__Http_Response.status
        else:
            return 404

    def before_request(self, *args, **kwargs):
        global Initial_Flag
        Initial_Flag += 1
        print("Initial process.")

    def request_done(self, result):
        global Done_Flag
        Done_Flag += 1
        print("Task done! ")
        return result

    def request_final(self):
        global Final_Flag
        Final_Flag += 1
        print("Task done! ")

    def request_error(self, error):
        global Exception_Flag
        Exception_Flag += 1
        print("Got failure when run task.")
        return error

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

    def test_request(self, *args, **kwargs):
        set_retry(RETRY_TIMES)
        http_cls = _TestRetryRequestsHTTP()
        # It will raise TimeoutError if it doesn't get response after 5 seconds later.
        # And it will retry to send HTTP request if it got any exception util overrate the retry times.
        response = http_cls.request(timeout=REQUEST_TIMEOUT)
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

