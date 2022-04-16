from multirunnable.persistence.file.archivers import Archiver
from multirunnable.persistence.file.files import File
from multirunnable.persistence.file.saver import FileSaver, ArchiverSaver
from multirunnable.persistence.file.layer import BaseFao
from multirunnable.persistence.file import SavingStrategy, SavingMediator
from abc import ABC



class BaseCrawlerFao(BaseFao, ABC):
    pass

