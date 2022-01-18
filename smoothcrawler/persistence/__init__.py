from abc import ABCMeta, abstractmethod



class PersistenceFacade(metaclass=ABCMeta):

    @abstractmethod
    def save(self, data, *args, **kwargs):
        pass

