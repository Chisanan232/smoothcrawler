from smoothcrawler.persistence.interface import DataPersistenceLayer

from abc import ABCMeta, abstractmethod, ABC



class FileAccessObject(DataPersistenceLayer, ABC):

    def __init__(self, **kwargs):
        super(FileAccessObject, self).__init__(**kwargs)
        self._path = kwargs.get("path", "")
        self._mode = kwargs.get("mode", "")



class CrawlerFao(FileAccessObject):

    pass

