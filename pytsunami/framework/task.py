from pytsunami.framework.factory import BaseCrawlerFactory

from abc import ABCMeta, abstractmethod



class BaseTask(metaclass=ABCMeta):

    pass



class BaseCrawler(BaseTask):

    def __init__(self, factory: BaseCrawlerFactory):
        self._http_sender = factory.http_sender()
        self._parser = factory.parser()
        self._data_handler = factory.data_handler()
        self._persistence = factory.persistence()


    @abstractmethod
    def run(self):
        pass



class Crawler(BaseCrawler):

    def run(self):
        __response = self._http_sender.send()
        __data = self._parser.parse(response=__response)
        __data = self._data_handler.data_handling(data=__data)
        self._persistence.save(data=__data)

