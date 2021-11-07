from smoothcrawler.persistence.mode import PersistenceMode, DatabaseDriver

from abc import ABCMeta, abstractmethod
from typing import List
import configparser
import pathlib
import os



class PropertiesUtil:

    __Properties_Utils_Instance = None
    __Properties_Key = "smoothcrawler"

    _Config_Parser: configparser.RawConfigParser = None
    _Config_Parser_Encoding: str = "utf-8"

    def __new__(cls, *args, **kwargs):
        if cls.__Properties_Utils_Instance is None:
            return super(PropertiesUtil, cls).__new__(cls)
        return cls.__Properties_Utils_Instance


    def __init__(self, mode: PersistenceMode, config_path: str, **kwargs):
        self.mode = mode
        if self.mode is PersistenceMode.DATABASE:
            db_driver_obj: DatabaseDriver = kwargs.get("database_driver", None)
            if db_driver_obj is None:
                raise ValueError("Parameter 'database_driver' shouldn't be empty if mode is DATABASE mode. ")
            else:
                self.db_driver = db_driver_obj.value.get("properties_key", None)
                if self.db_driver is None:
                    raise ValueError("The value in one specific DATABASE mode should have valid value.")

        __isfile = os.path.isfile(path=config_path)
        if __isfile:
            __config_file_path = config_path
        else:
            raise FileNotFoundError

        self.__Config_Parser = configparser.RawConfigParser()
        ## Method 1.
        # file = open(config_file, encoding="utf-8")
        # self.__Config_Parser.read_file(file, config_file)
        ## Method 2.
        self.__Config_Parser.read(
            filenames=__config_file_path,
            encoding=self._Config_Parser_Encoding
        )


    def get_value_as_str(self, property_key: str, group: str = "") -> str:
        __group = PropertiesUtil._get_properties_group(group=group)
        return self.__Config_Parser.get(__group, property_key)


    def get_value_as_list(self, property_key: str, group: str = "", separate: str = ",") -> List[str]:
        __group = PropertiesUtil._get_properties_group(group=group)
        return self.__Config_Parser.get(__group, property_key).split(separate)


    @staticmethod
    def _get_properties_group(group: str) -> str:
        return group[0].upper() + group[1:]


    def property_key(self) -> str:
        """
        Description:
            Get the configuration properties key.
        :return:
        """
        property_key = self.__Properties_Key
        if self.mode == PersistenceMode.DATABASE:
            __db_key = self.mode.value.get("properties_key")
            return ".".join([property_key, __db_key, self.db_driver])
            # return f"{property_key}.{__properties_key}.{db_driver}."
        else:
            __file_key = self.mode.value.get("properties_key")
            return ".".join([property_key, __file_key])



class BaseConfiguration(metaclass=ABCMeta):

    pass



class BaseDatabaseConfiguration(BaseConfiguration):

    @property
    @abstractmethod
    def host(self) -> str:
        """
        Description:
            Get host.
        :return:
        """
        pass


    @property
    @abstractmethod
    def port(self) -> str:
        """
        Description:
            Get port.
        :return:
        """
        pass


    @property
    @abstractmethod
    def username(self) -> str:
        """
        Description:
            Get username.
        :return:
        """
        pass


    @property
    @abstractmethod
    def password(self) -> str:
        """
        Description:
            Get password.
        :return:
        """
        pass


    @property
    @abstractmethod
    def database(self) -> str:
        """
        Description:
            Get database.
        :return:
        """
        pass



class BaseFileConfiguration(BaseConfiguration):

    @property
    @abstractmethod
    def formatter(self) -> List[str]:
        pass


    @formatter.setter
    @abstractmethod
    def formatter(self, formatter: str) -> None:
        pass


    @property
    @abstractmethod
    def name(self) -> str:
        pass


    @name.setter
    @abstractmethod
    def name(self, name: str) -> None:
        pass


    @property
    @abstractmethod
    def saving_directory(self) -> str:
        pass


    @saving_directory.setter
    @abstractmethod
    def saving_directory(self, file_dir: str) -> None:
        pass



class BaseArchiverConfiguration(BaseConfiguration):

    @property
    @abstractmethod
    def formatter(self) -> List[str]:
        pass


    @formatter.setter
    @abstractmethod
    def formatter(self, formatter: List[str]) -> None:
        pass


    @property
    @abstractmethod
    def name(self) -> str:
        pass


    @name.setter
    @abstractmethod
    def name(self, name: str) -> None:
        pass


    @property
    @abstractmethod
    def path(self) -> str:
        pass


    @path.setter
    @abstractmethod
    def path(self, path: str) -> None:
        pass

