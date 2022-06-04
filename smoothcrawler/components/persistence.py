from abc import ABCMeta, abstractmethod
from typing import Union, TypeVar, Generic, Iterable, Any


T = TypeVar("T")


class PersistenceFacade(metaclass=ABCMeta):

    @abstractmethod
    def save(self, data: Union[Iterable, Any], *args, **kwargs) -> Generic[T]:
        """
        Save the data, no matter save it as one specific file format or insert into database.

        :param data: The target data which would be saved. In generally, it's an iterator object.
        :return: In generally, it doesn't return anything. But it does if it needs.
        """

        pass

