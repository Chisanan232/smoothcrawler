from enum import Enum


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



from .mediator import SavingMediator
from .saver import FileSaver, ArchiverSaver
from .files import File, CSVFormatter, XLSXFormatter, JSONFormatter
from .archivers import Archiver, ZIPArchiver

