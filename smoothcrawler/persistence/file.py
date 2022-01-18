from abc import ABC
from multirunnable.persistence.file import SavingStrategy, SavingMediator
from multirunnable.persistence.file.files import File
from multirunnable.persistence.file.archivers import Archiver
from multirunnable.persistence.file.saver import FileSaver, ArchiverSaver
from multirunnable.persistence.file.layer import BaseFao



class BaseCrawlerFao(BaseFao, ABC):
    pass

