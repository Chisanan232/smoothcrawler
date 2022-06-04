from multipledispatch import dispatch
from typing import List, Tuple, Iterable, Union, Optional
from datetime import datetime, timedelta
from abc import ABCMeta, abstractmethod
import logging
import re


OPTION_VAR_INDEX: str = "index"
"""The option setting character of index."""

OPTION_VAR_DATE: str = "date"
"""The option setting character of date."""

OPTION_VAR_DATETIME: str = "datetime"
"""The option setting character of datetime."""

OPTION_VAR_ITERATOR: str = "iterator"
"""The option setting character of iterator."""


def get_option() -> Tuple:
    """
    Get all types of option which could be write in URL character.

    :return: A tuple of all option types.
    """

    return OPTION_VAR_INDEX, OPTION_VAR_DATE, OPTION_VAR_DATETIME, OPTION_VAR_ITERATOR


def set_index_rule() -> str:
    """
    Get the index option.
    The index option would iterate to generate URLs with index (1, 2, 3, ...).

    :return: The setting string of index option.
    """

    return OPTION_VAR_INDEX


def set_date_rule() -> str:
    """
    Get the date option. In generally, it's yyyymmdd. It only has year, month and day.
    It could iterator to generate  URLs with date (for example, 20210101, 20210102, ...).

    :return: The setting string of date option.
    """

    return OPTION_VAR_DATE


def set_datetime_rule() -> str:
    """
    Get the datetime option. In generally, it's yyyymmddhhMMss. It has year, month, day,
    hour, minute and second.
    It could iterator to generate  URLs with datetime (for example, 20210101000000, 20210101000001, ...).

    :return: The setting string of datetime option.
    """

    return OPTION_VAR_DATETIME


def set_iterator_rule() -> str:
    """
    Get the iterator option.
    It could iterator to generate  URLs with target iterator object.

    :return: The setting string of iterator option.
    """

    return OPTION_VAR_ITERATOR



class BaseURL(metaclass=ABCMeta):

    @property
    @abstractmethod
    def base_url(self) -> str:
        """
        An URL value. It could contain one of specific options (OPTION_VAR_INDEX, OPTION_VAR_DATE,
        OPTION_VAR_DATETIME and OPTION_VAR_ITERATOR) and it would be generated with the option meaning
        value. For example, it could set *base_url* as 'https://www.google.com?date={date}'. The
        URL be generated would be like 'https://www.google.com?date=20220601'.

        :return: An URL string value.
        """
        pass


    @abstractmethod
    def generate(self) -> List[str]:
        """
        Generating all the URLs we need base on the options.

        :return: A collection of URLs.
        """
        pass



class URL(BaseURL):

    __Base_Url: str = None
    __URLs: List[str] = []

    def __init__(self, base: str, start: Optional[Union[int, str]] = None, end: Optional[Union[int, str]] = None, formatter: str = "yyyymmdd", iter: Optional[Iterable] = None):
        if base == "" or base is None:
            raise ValueError("Foundational URL cannot be empty.")
        self.__Base_Url: str = base

        # Check the character of variable.
        self.option_is_index = re.search(r"\{" + re.escape(OPTION_VAR_INDEX) + "\}", base)
        self.option_is_date = re.search(r"\{" + re.escape(OPTION_VAR_DATE) + "\}", base)
        self.option_is_datetime = re.search(r"\{" + re.escape(OPTION_VAR_DATETIME) + "\}", base)
        self.option_is_iterator = re.search(r"\{" + re.escape(OPTION_VAR_ITERATOR) + "\}", base)

        self.start: Optional[Union[int, str]] = start
        self.end: Optional[Union[int, str]] = end
        self.formatter: str = formatter
        self.iterator: Iterable = iter

        self._start_date = None
        self._end_date = None
        self._diff_days = None
        self._period_days = 1
        self._period_hours = 0
        self._period_minutes = 0
        self._period_seconds = 0

        self._option: str = None
        self.urls: List = []


    @property
    def base_url(self) -> str:
        return self.__Base_Url


    @base_url.setter
    def base_url(self, url: str) -> None:
        self.__Base_Url = url


    def is_index_rule(self) -> bool:
        """
        Check the option setting of current URL object is index type.

        :return: It returns True if it is, or it returns False.
        """

        return self.option_is_index is not None


    def is_date_rule(self) -> bool:
        """
        Check the option setting of current URL object is date type.

        :return: It returns True if it is, or it returns False.
        """

        return self.option_is_date is not None


    def is_datetime_rule(self) -> bool:
        """
        Check the option setting of current URL object is datetime type.

        :return: It returns True if it is, or it returns False.
        """

        return self.option_is_datetime is not None


    def is_iterator_rule(self) -> bool:
        """
        Check the option setting of current URL object is iterator type.

        :return: It returns True if it is, or it returns False.
        """

        return self.option_is_iterator is not None


    def is_valid(self) -> bool:
        """
        Check the option setting of current URL object is valid.

        :return: It returns True if it is, or it returns False.
        """

        return self.is_index_rule() or \
               self.is_date_rule() or \
               self.is_datetime_rule() or \
               self.is_iterator_rule()


    @property
    def period_days(self) -> int:
        """
        Get the day value of period.

        :return: Return day value and it's a int type data.
        """

        return self._period_days


    @property
    def period_hours(self) -> int:
        """
        Get the hour value of period.

        :return: Return hour value and it's a int type data.
        """

        return self._period_hours


    @property
    def period_minutes(self) -> int:
        """
        Get the minute value of period.

        :return: Return minute value and it's a int type data.
        """

        return self._period_minutes


    @property
    def period_seconds(self) -> int:
        """
        Get the second value of period.

        :return: Return second value and it's a int type data.
        """

        return self._period_seconds


    def set_period(self, days: Optional[int] = None, hours: Optional[int] = None, minutes: Optional[int] = None, seconds: Optional[int] = None) -> None:
        """
        Configure the period settings like how many days, hours, minutes or seconds.

        :param days: How many days to iterate next value.
        :param hours: How many hours to iterate next value.
        :param minutes: How many minutes to iterate next value.
        :param seconds: How many seconds to iterate next value.
        :return: None
        """

        if days is not None:
            self._period_days = days
        if hours is not None:
            self._period_hours = hours
        if minutes is not None:
            self._period_minutes = minutes
        if seconds is not None:
            self._period_seconds = seconds


    def generate(self) -> List[str]:
        if self.option_is_index:
            # Check whether the needed option id ready or not.
            if self.start is None and self.end is None:
                raise ValueError("Options *start* and *end* cannot be empty value with INDEX rule.")

            if type(self.start) is not int or type(self.end) is not int:
                logging.warning("The types of start index and end index aren't 'int'. It will try to convert to 'int' type.")
                try:
                    self.start = int(self.start)
                    self.end = int(self.end)
                except ValueError as e:
                    raise ValueError("Parameter *start* and *end* should be integers or integer type characters.")

            self._index_handling(index=self.start)

        elif self.option_is_date:
            if self.start is None and self.end is None:
                raise ValueError("Options *start* and *end* cannot be empty value with DATE rule.")

            if type(self.start) is not str or type(self.end) is not str:
                raise ValueError("The value format is incorrect of options *start* and *end*.")

            chksum = URL._is_py_datetime_format(formatter=self.formatter)
            if chksum is True:
                formatter = self.formatter
            else:
                formatter = URL._convert_formatter(formatter=self.formatter)
            self._start_date = datetime.strptime(self.start, formatter)
            self._end_date = datetime.strptime(self.end, formatter)
            self._diff_days = (self._end_date.date() - self._start_date.date()).days

            self._date_handling(_date=self._start_date, days=self.period_days)

        elif self.option_is_datetime:
            if self.start is None and self.end is None:
                raise ValueError("Options *start* and *end* cannot be empty value with DATETIME rule.")

            if type(self.start) is not str or type(self.end) is not str:
                raise ValueError("The value format is incorrect of options *start* and *end*.")

            chksum = URL._is_py_datetime_format(formatter=self.formatter)
            if chksum is True:
                formatter = self.formatter
            else:
                formatter = URL._convert_formatter(formatter=self.formatter)
            self._start_date = datetime.strptime(self.start, formatter)
            self._end_date = datetime.strptime(self.end, formatter)
            self._diff_days = (self._end_date - self._start_date).days

            self._datetime_handling(
                _datetime=self._start_date,
                days=self.period_days,
                hours=self.period_hours,
                minutes=self.period_minutes,
                seconds=self.period_seconds)

        elif self.option_is_iterator:
            if self.iterator is None:
                raise ValueError("Options *iterator* cannot be empty value with ITERATOR rule.")

            self._iterator_handling(self.iterator)

        else:
            raise ValueError("Cannot verify the option variable. Please using '{%s}', '{%s}', '{%s}' or '{%s}'.",
                             OPTION_VAR_INDEX, OPTION_VAR_DATE, OPTION_VAR_DATETIME, OPTION_VAR_ITERATOR)

        return self.urls


    def _index_handling(self, index: int) -> None:
        """
        The main process to generate URL with index.

        :param index: The index value. It should be a started number.
        :return: None
        """

        if index <= self.end:
            option = URL._add_flag(option=OPTION_VAR_INDEX)
            target_url = self.base_url.replace(option, str(index))
            self.urls.append(target_url)
            self._index_handling(index=index + 1)


    @staticmethod
    def _is_py_datetime_format(formatter: str) -> bool:
        """
        Check whether the character format of datetime formatter is valid or not.

        :param formatter: The character format of datetime formatter. It's usage could refer below:

                                    +-----------+------------+
                                    | Formatter |   Meaning  |
                                    +===========+============+
                                    |    %Y     |     year   |
                                    +-----------+------------+
                                    |    %m     |    month   |
                                    +-----------+------------+
                                    |    %d     |     day    |
                                    +-----------+------------+
                                    |    %H     |     hour   |
                                    +-----------+------------+
                                    |    %M     |    minute  |
                                    +-----------+------------+
                                    |    %S     |    second  |
                                    +-----------+------------+

        :return: It returns True if the character format of datetime formatter is valid, or it return False.
        """

        def chk_char(t_ele) -> bool:
            res = re.search(r"[Y,m,d,H,M,S]", t_ele)
            if res is not None:
                return True
            else:
                return False

        if "%" in formatter:
            chk_result = map(chk_char, formatter.split("%"))
            if False in chk_result:
                return False
            else:
                return True
        else:
            return False


    @staticmethod
    def _convert_formatter(formatter: str) -> str:
        """
        About parameter *formatter*, it could be like below:
        1. yyyymmdd, example: 20210101
        2. yyyy/mm/dd, example: 2021/01/01
        3. yyyy-mm-dd, example: 2021-01-01

        :param formatter: The character format of datetime formatter.
        :return: A string type value which be formatted with the date or datetime format.
        """

        year_format = re.search(r"yyyy", formatter, re.IGNORECASE)
        month_format = re.search(r"mm", formatter)
        day_format = re.search(r"dd", formatter, re.IGNORECASE)
        hour_format = re.search(r"HH", formatter)
        minute_format = re.search(r"MM", formatter)
        second_format = re.search(r"SS", formatter)

        # Check the split characters
        date_split_char = re.search(r"[-/]", formatter)
        if date_split_char is not None:
            date_split_char = date_split_char.group(0)
            if len(date_split_char) > 1:
                raise ValueError("")
        else:
            date_split_char = ""

        time_split_char = re.search(r"[:]", formatter)
        if time_split_char is not None:
            time_split_char = time_split_char.group(0)
        else:
            time_split_char = ""

        # Check the empty space
        empty_flag = False
        formatters = formatter.split(" ")
        if len(formatters) > 2:
            raise ValueError(f"It exists more than 2 empty spaces. It's unnatural and please check the value (error value is {formatter}).")
        if len(formatters) == 2:
            # Has an empty space
            empty_flag = True

        date_parsers = []
        time_parsers = []
        if year_format is not None:
            date_parsers.append("%Y")
        if month_format is not None:
            date_parsers.append("%m")
        if day_format is not None:
            date_parsers.append("%d")
        if hour_format is not None:
            time_parsers.append("%H")
        if minute_format is not None:
            time_parsers.append("%M")
        if second_format is not None:
            time_parsers.append("%S")

        date_formatter = date_split_char.join(date_parsers)
        time_formatter = time_split_char.join(time_parsers)
        if empty_flag is True:
            final_formatter = " ".join([date_formatter, time_formatter])
        else:
            if time_formatter:
                final_formatter = "".join([date_formatter, time_formatter])
            else:
                final_formatter = date_formatter

        return final_formatter


    def _date_handling(self, _date: datetime, days: int) -> None:
        """
        The main process to generate URL with date.

        :param _date: A datetime object.
        :param days: How many days to iterate next value.
        :return: None
        """

        if _date <= self._end_date:
            date_option_val = _date.strftime("%Y%m%d").replace("-", "")

            option = URL._add_flag(option=OPTION_VAR_DATE)
            target_url = self.base_url.replace(option, date_option_val)
            self.urls.append(target_url)

            new_date = _date + timedelta(days=days)
            self._date_handling(_date=new_date, days=days)


    def _datetime_handling(self, _datetime: datetime, days: int = None, hours: int=None, minutes: int=None, seconds: int=None) -> None:
        """
        The main process to generate URL with datetime.

        :param _datetime:
        :param days: How many days to iterate next value.
        :param hours: How many hours to iterate next value.
        :param minutes: How many minutes to iterate next value.
        :param seconds: How many seconds to iterate next value.
        :return: None
        """

        if _datetime <= self._end_date:
            date_option_val = _datetime.isoformat().replace("-", "")
            date_option_val = date_option_val.replace(":", "")
            date_option_val = date_option_val.replace("T", "")

            option = URL._add_flag(option=OPTION_VAR_DATETIME)
            target_url = self.base_url.replace(option, date_option_val)
            self.urls.append(target_url)

            new_datetime = _datetime + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
            self._datetime_handling(_datetime=new_datetime, days=days, hours=hours, minutes=minutes, seconds=seconds)


    @dispatch((list, tuple, set))
    def _iterator_handling(self, iter: Union[list, tuple, set]) -> None:
        """
        The main process to generate URL with iterator. This overload function run process
        if the option *iter* is *list*, *tuple* or *set* type.

        :param iter: A iterator. It could be a *list*, *tuple* or *set* type.
        :return: None
        """

        for ele in iter:
            option = URL._add_flag(option=OPTION_VAR_ITERATOR)
            target_url = self.base_url.replace(option, str(ele))
            self.urls.append(target_url)


    @dispatch(dict)
    def _iterator_handling(self, iter: dict) -> None:
        """
        Description:
            The main process to generate URL with iterator. This overload function run process
        if the option *iter* is *dict* type.
            It could all data content which be saved in received parameter
            combine the key and value as HTTP GET method format options.

        Example:
            Received parameter value:
                {"index_1": 1, "index_2": 2}
            Result:
                index_1=1, index_2=2

        :param iter: A iterator. It could be a *dict type.
        :return: None
        """
        for key, val in iter.items():
            option = URL._add_flag(option=OPTION_VAR_ITERATOR)
            target_url = self.base_url.replace(option, f"{key}={val}")
            self.urls.append(target_url)


    @staticmethod
    def _add_flag(option: str) -> str:
        """
        Get the character with the option and the specific format it defines.

        :param option: The option setting.
        :return: A string value.
        """

        return "{" + option + "}"


