from typing import List
from enum import Enum
import re


_Super_Worker_Saving_File_Key = "main_save_file"
_Sub_Worker_Saving_File_Key = "child_save_file"
_Activate_Compress_Key = "compress"


class SavingStrategy(Enum):

    ONE_THREAD_ONE_FILE = {
        _Super_Worker_Saving_File_Key: False,
        _Sub_Worker_Saving_File_Key: True,
        _Activate_Compress_Key: False
    }

    ALL_THREADS_ONE_FILE = {
        _Super_Worker_Saving_File_Key: True,
        _Sub_Worker_Saving_File_Key: False,
        _Activate_Compress_Key: False
    }

    ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL = {
        _Super_Worker_Saving_File_Key: True,
        _Sub_Worker_Saving_File_Key: True,
        _Activate_Compress_Key: True
    }



from smoothcrawler.persistence.file.mediator import BaseMediator as _BaseMediator, SavingMediator
from smoothcrawler.persistence.file.saver import FileSaver, ArchiverSaver
from smoothcrawler.persistence.file.files import File, CSVFormatter, XLSXFormatter, JSONFormatter
from smoothcrawler.persistence.file.archivers import ZIPArchiver
from smoothcrawler.persistence.file.layer import DataPersistenceLayer
from smoothcrawler.persistence.file.layer import FileAccessObject
from smoothcrawler._utils import ImportModule



class FileFormat(Enum):

    CSV = {
        "package": ".persistence.file",
        "formatter": "CSVFormatter"
    }
    XLSX = {
        "package": ".persistence.file",
        "formatter": "XLSXFormatter"
    }
    JSON = {
        "package": ".persistence.file",
        "formatter": "JSONFormatter"
    }



class PersistenceFacade:

    _Mediator: _BaseMediator = None
    _Strategy: SavingStrategy = None

    def __init__(self, mediator: _BaseMediator, strategy: SavingStrategy):
        self._Mediator = mediator
        self._Strategy = strategy


    def save_as_file(self, file: str, mode: str, data: List[list]):
        is_valid_format = re.search(r"\w{1,128}\.[csv,xlsx,json]", file)
        if is_valid_format:
            file_formatter = is_valid_format.group(0).upper()
            ImportModule.get_class(pkg_name=".persistence.file", cls_name=f"{file_formatter}Formatter")
            file_saver = FileSaver(file=CSVFormatter())
        else:
            file_format = file.split("\.")[-1]
            raise TypeError(f"It doesn't support file format '{file_format}' currently.")

        file_saver.register(mediator=self._Mediator, strategy=self._Strategy)
        result = file_saver.save(file=file, mode=mode, data=data)
        return result


    def compress_data(self, file: str, mode: str, data: List):
        if self._Strategy is not SavingStrategy.ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL:
            raise ValueError("The compress process only work with strategy 'ONE_THREAD_ONE_FILE_AND_COMPRESS_ALL'.")

        is_zip = re.search(r"\w{1,128}\.zip", file)
        if is_zip:
            archiver_saver = ArchiverSaver(archiver=ZIPArchiver())
        else:
            archiver_format = file.split("\.")[-1]
            raise TypeError(f"It doesn't support archiver format '{archiver_format}' currently.")

        archiver_saver.register(mediator=self._Mediator, strategy=self._Strategy)
        archiver_saver.compress(file=file, mode=mode, data=data)


