from smoothcrawler.components.httpio import HTTP
from abc import ABCMeta, abstractmethod
import urllib3
import logging
import random
import pytest
import http


HTTP_METHOD = "GET"
TEST_URL = "https://www.google.com"
# TEST_URL = "https://www.youtube.com"
TEST_TIMEOUT_URL = "https://www.test.com"

RETRY_TIMES = 3
REQUEST_TIMEOUT = 5

GET_FLAG = False
POST_FLAG = False
PUT_FLAG = False
DELETE_FLAG = False
HEAD_FLAG = False
OPTION_FLAG = False

Test_Http_Logger = logging.getLogger("smoothcrawler.http_io")
stream_logger = logging.StreamHandler()
stream_logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s %(module)s.%(funcName)s(): %(levelname)-8s %(message)s')
stream_logger.setFormatter(formatter)
Test_Http_Logger.addHandler(stream_logger)


def init_flag():
    global GET_FLAG, POST_FLAG, PUT_FLAG, DELETE_FLAG, HEAD_FLAG, OPTION_FLAG

    GET_FLAG = False
    POST_FLAG = False
    PUT_FLAG = False
    DELETE_FLAG = False
    HEAD_FLAG = False
    OPTION_FLAG = False


class _TestRequestsHTTP(HTTP):

    __Http_Response = None

    def request(self, url, method="GET", timeout=-1, *args, **kwargs):
        Test_Http_Logger.info("Send HTTP request by 'urllib3'.")
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request(HTTP_METHOD, url)
        return self.__Http_Response


    @property
    def status_code(self):
        if self.__Http_Response:
            return self.__Http_Response.status
        else:
            return -1



class _TestMethodsHTTP(HTTP):

    __Http_Response = None

    def get(self, url: str, *args, **kwargs):
        global GET_FLAG
        GET_FLAG = True
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("GET", url)
        return self.__Http_Response


    def post(self, url: str, *args, **kwargs):
        global POST_FLAG
        POST_FLAG = True
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("POST", url)
        return self.__Http_Response


    def put(self, url: str, *args, **kwargs):
        global PUT_FLAG
        PUT_FLAG = True
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("PUT", url)
        return self.__Http_Response


    def delete(self, url: str, *args, **kwargs):
        global DELETE_FLAG
        DELETE_FLAG = True
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("DELETE", url)
        return self.__Http_Response


    def head(self, url: str, *args, **kwargs):
        global HEAD_FLAG
        HEAD_FLAG = True
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("HEAD", url)
        return self.__Http_Response


    def option(self, url: str, *args, **kwargs):
        global OPTION_FLAG
        OPTION_FLAG = True
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("OPTION", url)
        return self.__Http_Response


    @property
    def status_code(self):
        if self.__Http_Response:
            return self.__Http_Response.status
        else:
            return -1



class _TestWrongMethodsHTTP(HTTP):
    __Http_Response = None

    def no_get(self, url, *args, **kwargs):
        global GET_FLAG
        GET_FLAG = True
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("GET", url)
        logging.debug("New get implementation.")
        logging.debug(f"Response: {self.__Http_Response}")
        return self.__Http_Response


    def no_post(self, url, *args, **kwargs):
        global POST_FLAG
        POST_FLAG = True
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("POST", url)
        return self.__Http_Response


    def no_put(self, url, *args, **kwargs):
        global PUT_FLAG
        PUT_FLAG = True
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("PUT", url)
        return self.__Http_Response


    def no_delete(self, url, *args, **kwargs):
        global DELETE_FLAG
        DELETE_FLAG = True
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("DELETE", url)
        return self.__Http_Response


    def no_head(self, url, *args, **kwargs):
        global HEAD_FLAG
        HEAD_FLAG = True
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("HEAD", url)
        return self.__Http_Response


    def no_option(self, url, *args, **kwargs):
        global OPTION_FLAG
        OPTION_FLAG = True
        _http = urllib3.PoolManager()
        self.__Http_Response = _http.request("OPTION", url)
        return self.__Http_Response


Test_Sleep_Time = REQUEST_TIMEOUT + RETRY_TIMES - 1

Initial_Flag = 0
Done_Flag = 0
Final_Flag = 0
Exception_Flag = 0


def reset_counter():
    global Initial_Flag, Done_Flag, Final_Flag, Exception_Flag
    Initial_Flag = 0
    Done_Flag = 0
    Final_Flag = 0
    Exception_Flag = 0



class _TestRetryRequestsHTTP(HTTP):

    """
    A sample code for implementing some features of HTTP.
    """

    __Fail_Mode = None
    __Http_Response = None

    def __init__(self, fail_mode: bool = False):
        super().__init__()
        self.__Fail_Mode = fail_mode


    def get(self, url, *args, **kwargs):
        if self.__Fail_Mode is True:
            raise TimeoutError("For testing")
        else:
            _http = urllib3.PoolManager()
            self.__Http_Response = _http.request("GET", url)
            return self.__Http_Response


    def before_request(self, *args, **kwargs):
        global Initial_Flag
        print("[DEBUG in _TestRetryRequestsHTTP.before_request_new]")
        Initial_Flag += 1
        Test_Http_Logger.info("Initial task process.")


    def request_done(self, result):
        global Done_Flag
        print("[DEBUG in _TestRetryRequestsHTTP.request_done_new]")
        Done_Flag += 1
        Test_Http_Logger.info("Task done! ")
        return result


    def request_fail(self, error: Exception):
        global Exception_Flag
        print("[DEBUG in _TestRetryRequestsHTTP.request_fail_new]")
        Exception_Flag += 1
        Test_Http_Logger.info("Got failure when run task.")
        return error


    def request_final(self):
        global Final_Flag
        print("[DEBUG in _TestRetryRequestsHTTP.request_final_new]")
        Final_Flag += 1
        Test_Http_Logger.info("Task done! ")


    @property
    def status_code(self):
        if self.__Http_Response:
            return self.__Http_Response.status
        else:
            Test_Http_Logger.warning("There is no HTTP response currently.")
            return -1


    def http_200_response(self, response):
        Test_Http_Logger.info("Get the HTTP response successfully.")



class BaseHttpTestSpec(metaclass=ABCMeta):
    """
    Test Description:
        Testing method 'request' feature, including parameter 'method', 'timeout'

    Test cases:
        Parameter 'url':
            str type:
            URL type:
            other type: raise ValueError.

        Parameter 'method':
            'GET': It should send HTTP request via 'GET' method.
            'POST': It should send HTTP request via 'POST' method.
            'PUT': It should send HTTP request via 'PUT' method.
            'DELETE': It should send HTTP request via 'DELETE' method.
            'HEAD': It should send HTTP request via 'HEAD' method.
            'OPTION': It should send HTTP request via 'OPTION' method.

        Note about testing case of 'method':
            Annotate again, this package DOES NOT case about how developers implement HTTP request (GET, POST, etc).
            It only cares about the software architecture. That's the reason why we just need to check it work in this package design except feature.

        Parameter 'timeout':
            -1: It would doesn't timeout and keep waiting for the response util request timeout.
            <-1: It will raise an ValueError.
            >=0: It would timeout after the time period.

        Parameter 'retry_components':
            'before_request': It should be run before it send HTTP request.
            'request_done': It should be run after it send HTTP request and get the HTTP response.
            'request_final': It must to run this implementation no matter whether it run successfully or not.
            'request_error': It would be run if it gets anything exception when it sends HTTP request.
    """

    @abstractmethod
    def test_request_url(self, *args, **kwargs):
        """
        Test Description:
        Parameter 'url':
            str type:
            URL type:
            other type: raise ValueError.
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def test_request_method(self, *args, **kwargs):
        """
        Test Description:
        Parameter 'method' of bounded function 'test_request_method' of module 'HTTP':
            'GET': It should send HTTP request via 'GET' method.
            'POST': It should send HTTP request via 'POST' method.
            'PUT': It should send HTTP request via 'PUT' method.
            'DELETE': It should send HTTP request via 'DELETE' method.
            'HEAD': It should send HTTP request via 'HEAD' method.
            'OPTION': It should send HTTP request via 'OPTION' method.
        :param args:
        :param kwargs:
        :return:
        """
        pass


    @abstractmethod
    def test_request_timeout(self):
        """
        Test Description:
        Parameter 'timeout':
            -1: It would doesn't timeout and keep waiting for the response util request timeout.
            <-1: It will raise an ValueError.
            >=0: It would timeout after the time period.
        :return:
        """
        pass


    @abstractmethod
    def test_request_retry(self):
        """
        Test Description:
        Parameter 'retry_components':
            'before_request': It should be run before it send HTTP request.
            'request_done': It should be run after it send HTTP request and get the HTTP response.
            'request_final': It must to run this implementation no matter whether it run successfully or not.
            'request_error': It would be run if it gets anything exception when it sends HTTP request.
        :return:
        """
        pass


    @abstractmethod
    def test_get(self):
        pass


    @abstractmethod
    def test_post(self):
        pass


    @abstractmethod
    def test_put(self):
        pass


    @abstractmethod
    def test_delete(self):
        pass


    @abstractmethod
    def test_head(self):
        pass


    @abstractmethod
    def test_option(self):
        pass



class TestHttp(BaseHttpTestSpec):

    @pytest.mark.skip(reason="No implement testing logic.")
    def test_request_url(self, *args, **kwargs):
        pass


    def test_request_method(self, *args, **kwargs):
        req_ver_http = _TestRequestsHTTP()
        req_response = req_ver_http.request(url=TEST_URL)
        assert req_response is not None, "It doesn't implement the code which has responsibility about sending HTTP request."
        assert req_ver_http.status_code is not None, "HTTP status code must to be a value."

        status_code = int(req_ver_http.status_code)
        assert TestHttp.__status_code_is_valid(status_code) is True, "This is not a valid status code."

        methods_http = _TestMethodsHTTP()
        # Test HTTP method 'GET'
        method_response = methods_http.request(url=TEST_URL, method="GET")
        assert method_response is not None, "It doesn't implement the code which has responsibility about sending HTTP request."
        __http_status = method_response.status
        assert __http_status is not None, "HTTP status code must to be a value."

        status_code = int(__http_status)
        assert TestHttp.__status_code_is_valid(status_code) is True, "This is not a valid status code."


    @pytest.mark.skip(reason="No implement testing logic.")
    def test_request_timeout(self):
        pass


    @pytest.mark.skip(reason="No implement testing logic.")
    def test_request_retry(self):
        pass


    def test_get(self):

        def final_assert():
            assert GET_FLAG is False, \
                f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        req_method = "GET"
        req_method_upper = req_method.upper()
        req_method_lower = req_method.lower()

        _http_cls = _TestMethodsHTTP()
        TestHttp.__test_request_with_upper_char(_http_cls, req_method)
        assert GET_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_replace_random_char(_http_cls, req_method)
        assert GET_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_insert_random_char(_http_cls, req_method)
        assert GET_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_invalid_char(_http_cls, final_assert)

        response = TestHttp.__request_with_no_override(req_method)
        assert GET_FLAG is False, \
            f"'HTTP.request' should not call function '{req_method.lower()}' because it doesn't override it."
        assert response is None, "The HTTP response result should be None in default."


    def test_post(self):

        def final_assert():
            assert POST_FLAG is False, \
                f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        req_method = "POST"
        req_method_upper = req_method.upper()
        req_method_lower = req_method.lower()

        _http_cls = _TestMethodsHTTP()
        TestHttp.__test_request_with_upper_char(_http_cls, req_method)
        assert POST_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_replace_random_char(_http_cls, req_method)
        assert POST_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_insert_random_char(_http_cls, req_method)
        assert POST_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_invalid_char(_http_cls, final_assert)

        response = TestHttp.__request_with_no_override(req_method)
        assert POST_FLAG is False, \
            f"'HTTP.request' should not call function '{req_method.lower()}' because it doesn't override it."
        assert response is None, "The HTTP response result should be None in default."


    def test_put(self):

        def final_assert():
            assert PUT_FLAG is False, \
                f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        req_method = "PUT"
        req_method_upper = req_method.upper()
        req_method_lower = req_method.lower()

        _http_cls = _TestMethodsHTTP()
        TestHttp.__test_request_with_upper_char(_http_cls, req_method)
        assert PUT_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_replace_random_char(_http_cls, req_method)
        assert PUT_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_insert_random_char(_http_cls, req_method)
        assert PUT_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_invalid_char(_http_cls, final_assert)

        response = TestHttp.__request_with_no_override(req_method)
        assert PUT_FLAG is False, \
            f"'HTTP.request' should not call function '{req_method.lower()}' because it doesn't override it."
        assert response is None, "The HTTP response result should be None in default."


    def test_delete(self):

        def final_assert():
            assert DELETE_FLAG is False, \
                f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        req_method = "DELETE"
        req_method_upper = req_method.upper()
        req_method_lower = req_method.lower()

        _http_cls = _TestMethodsHTTP()
        TestHttp.__test_request_with_upper_char(_http_cls, req_method)
        assert DELETE_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_replace_random_char(_http_cls, req_method)
        assert DELETE_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_insert_random_char(_http_cls, req_method)
        assert DELETE_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_invalid_char(_http_cls, final_assert)

        response = TestHttp.__request_with_no_override(req_method)
        assert DELETE_FLAG is False, \
            f"'HTTP.request' should not call function '{req_method.lower()}' because it doesn't override it."
        assert response is None, "The HTTP response result should be None in default."


    def test_head(self):

        def final_assert():
            assert HEAD_FLAG is False, \
                f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        req_method = "HEAD"
        req_method_upper = req_method.upper()
        req_method_lower = req_method.lower()

        _http_cls = _TestMethodsHTTP()
        TestHttp.__test_request_with_upper_char(_http_cls, req_method)
        assert HEAD_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_replace_random_char(_http_cls, req_method)
        assert HEAD_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_insert_random_char(_http_cls, req_method)
        assert HEAD_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_invalid_char(_http_cls, final_assert)

        response = TestHttp.__request_with_no_override(req_method)
        assert HEAD_FLAG is False, \
            f"'HTTP.request' should not call function '{req_method.lower()}' because it doesn't override it."
        assert response is None, "The HTTP response result should be None in default."


    def test_option(self):

        def final_assert():
            assert OPTION_FLAG is False, \
                f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        req_method = "OPTION"
        req_method_upper = req_method.upper()
        req_method_lower = req_method.lower()

        _http_cls = _TestMethodsHTTP()
        TestHttp.__test_request_with_upper_char(_http_cls, req_method)
        assert OPTION_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_replace_random_char(_http_cls, req_method)
        assert OPTION_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_insert_random_char(_http_cls, req_method)
        assert OPTION_FLAG is True, \
            f"'HTTP.request' should call function '{req_method_lower}' with option *method* value is '{req_method_upper}'."

        TestHttp.__test_request_with_invalid_char(_http_cls, final_assert)

        response = TestHttp.__request_with_no_override(req_method)
        assert OPTION_FLAG is False, \
            f"'HTTP.request' should not call function '{req_method.lower()}' because it doesn't override it."
        assert response is None, "The HTTP response result should be None in default."


    @staticmethod
    def __test_request_with_upper_char(http_cls, req_method: str):
        init_flag()

        req_method_upper = req_method.upper()

        response = http_cls.request(method=req_method_upper, url=TEST_URL)
        Test_Http_Logger.info(f"Test with option value '{req_method_upper}'.")


    @staticmethod
    def __test_request_with_replace_random_char(http_cls, req_method: str):
        init_flag()

        req_method_replace_random = TestHttp.__replace_random_char(target=req_method)

        response = http_cls.request(method=req_method_replace_random, url=TEST_URL)
        Test_Http_Logger.info(f"Test with option value '{req_method_replace_random}'.")


    @staticmethod
    def __test_request_with_insert_random_char(http_cls, req_method: str):
        init_flag()

        john_cena_char = "$%#%$%#%YouCAnNotSeeME"
        req_method_insert_random = TestHttp.__insert_random_char(target=john_cena_char, insert=req_method)

        # No sure that whether package should filter this characters or not
        response = http_cls.request(method=req_method_insert_random, url=TEST_URL)
        Test_Http_Logger.info(f"Test with option value '{req_method_insert_random}'.")


    @staticmethod
    def __test_request_with_invalid_char(http_cls, assert_callable):
        init_flag()

        magic_char = "$%##%NowYouSeeME"

        # Invalid option value
        request_exception = None
        try:
            request_exception = http_cls.request(method=magic_char, url=TEST_URL)
        except Exception as e:
            request_exception = e
        finally:
            Test_Http_Logger.info(f"Test with option value '{magic_char}'.")
            assert_callable()
            assert type(request_exception) is TypeError, \
                "'HTTP.request' should filter invalid option value."


    @staticmethod
    def __request_with_no_override(req_method: str):
        _http_cls = _TestWrongMethodsHTTP()
        response = _http_cls.request(method=req_method, url=TEST_URL)
        Test_Http_Logger.info(f"Test with option value '{req_method}'.")
        return response


    @staticmethod
    def __replace_random_char(target: str) -> str:
        replaced_char_index = random.randrange(0, len(target))
        if replaced_char_index % random.randrange(1, 2) == random.randrange(1, 2):
            target_random = target[:replaced_char_index] + target[replaced_char_index].upper() + target[replaced_char_index + 1:]
        else:
            target_random = target[:replaced_char_index] + target[replaced_char_index].lower() + target[replaced_char_index + 1:]
        return target_random


    @staticmethod
    def __insert_random_char(target: str, insert: str) -> str:
        insert_char_index = random.randrange(0, len(target))
        if insert_char_index % random.randrange(1, 2) == random.randrange(1, 2):
            target_random = target[:insert_char_index] + insert + target[insert_char_index:]
        else:
            target_random = target[:insert_char_index] + insert + target[insert_char_index:]
        return target_random


    def test_retry_mechanism_with_adapter(self):
        reset_counter()

        for test_mode in [True, False]:
            global Initial_Flag, Done_Flag, Final_Flag, Exception_Flag
            Initial_Flag = 0
            Done_Flag = 0
            Final_Flag = 0
            Exception_Flag = 0

            http_cls = _TestRetryRequestsHTTP(fail_mode=test_mode)
            response = http_cls.request(url=TEST_URL, timeout=RETRY_TIMES)
            TestHttp.__request_checking(test_mode, http_cls, response)


    @staticmethod
    def __request_checking(fail_mode, http_cls, response):
        assert response is not None, "It doesn't implement the code which has responsibility about sending HTTP request."
        if fail_mode is True:
            assert Initial_Flag == RETRY_TIMES, "Initial process times should be equal to retry times."
            assert Done_Flag == RETRY_TIMES or Exception_Flag == RETRY_TIMES, "The times of done process or exception handling process should be equal to retry times."
            assert Final_Flag == RETRY_TIMES, "Final process times should be equal to retry times."
        else:
            __http_status = response.status
            assert __http_status is not None, "HTTP status code must to be a value."

            status_code = int(__http_status)
            assert TestHttp.__status_code_is_valid(status_code) is True, "This is not a valid status code."

            assert Initial_Flag <= RETRY_TIMES, "Initial process times should be equal to retry times."
            assert Done_Flag <= RETRY_TIMES and \
                   Exception_Flag <= RETRY_TIMES and \
                   (Done_Flag + Exception_Flag) <= RETRY_TIMES, "The times of done process or exception handling process should be equal to retry times."
            assert Final_Flag <= RETRY_TIMES, "Final process times should be equal to retry times."


    @staticmethod
    def __status_code_is_valid(status):
        for _status in http.HTTPStatus:
            if int(status) == _status.value:
                return True
        else:
            return False

