from abc import ABCMeta, abstractmethod
from typing import List, Tuple, Iterable, Union, Optional
from multipledispatch import dispatch
from datetime import date, datetime, timedelta
import logging
import re


OPTION_VAR_INDEX: str = "index"
OPTION_VAR_DATE: str = "date"
OPTION_VAR_DATETIME: str = "datetime"
OPTION_VAR_ITERATOR: str = "iterator"


def get_option() -> Tuple:
    return OPTION_VAR_INDEX, OPTION_VAR_DATE, OPTION_VAR_DATETIME, OPTION_VAR_ITERATOR


def set_index_rule() -> str:
    return OPTION_VAR_INDEX


def set_date_rule() -> str:
    return OPTION_VAR_DATE


def set_datetime_rule() -> str:
    return OPTION_VAR_DATETIME


def set_iterator_rule() -> str:
    return OPTION_VAR_ITERATOR


class BaseURL(metaclass=ABCMeta):

    @property
    @abstractmethod
    def base_url(self) -> str:
        pass


    @abstractmethod
    def generate(self) -> List[str]:
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


    def is_index_rule(self) -> bool:
        return self.option_is_index is not None


    def is_date_rule(self) -> bool:
        return self.option_is_date is not None


    def is_datetime_rule(self) -> bool:
        return self.option_is_datetime is not None


    def is_iterator_rule(self) -> bool:
        return self.option_is_iterator is not None


    def is_valid(self) -> bool:
        return self.is_index_rule() or \
               self.is_date_rule() or \
               self.is_datetime_rule() or \
               self.is_iterator_rule()


    @property
    def period_days(self) -> int:
        return self._period_days


    @property
    def period_hours(self) -> int:
        return self._period_hours


    @property
    def period_minutes(self) -> int:
        return self._period_minutes


    @property
    def period_seconds(self) -> int:
        return self._period_seconds


    def set_period(self, days: Optional[int] = None, hours: Optional[int] = None, minutes: Optional[int] = None, seconds: Optional[int] = None) -> None:
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
                logging.warning(f"The types of start index and end index aren't 'int'. It will try to convert to 'int' type.")
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
        if index <= self.end:
            option = URL._add_flag(option=OPTION_VAR_INDEX)
            target_url = self.base_url.replace(option, str(index))
            self.urls.append(target_url)
            self._index_handling(index=index + 1)


    @staticmethod
    def _convert_formatter(formatter: str) -> str:
        """
        Description:
            About parameter *formatter*,
        :param formatter:
        :return:
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
        if _date <= self._end_date:
            date_option_val = _date.isoformat().replace("-", "")

            option = URL._add_flag(option=OPTION_VAR_DATE)
            target_url = self.base_url.replace(option, date_option_val)
            self.urls.append(target_url)

            new_date = _date + timedelta(days=days)
            self._date_handling(_date=new_date, days=days)


    def _datetime_handling(self, _datetime: datetime, days: int = None, hours: int=None, minutes: int=None, seconds: int=None) -> None:
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
        for ele in iter:
            option = URL._add_flag(option=OPTION_VAR_ITERATOR)
            target_url = self.base_url.replace(option, str(ele))
            self.urls.append(target_url)


    @dispatch(dict)
    def _iterator_handling(self, iter: dict) -> None:
        """
        Description:
            It could all data content which be saved in received parameter
            combine the key and value as HTTP GET method format options.

        Example:
            Received parameter value:
                {"index_1": 1, "index_2": 2}
            Result:
                index_1=1, index_2=2

        :param iter:
        :return:
        """
        for key, val in iter.items():
            option = URL._add_flag(option=OPTION_VAR_ITERATOR)
            target_url = self.base_url.replace(option, f"{key}={val}")
            self.urls.append(target_url)


    @staticmethod
    def _add_flag(option: str) -> str:
        return "{" + option + "}"


