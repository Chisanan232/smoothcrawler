from importlib import import_module
from typing import Callable
import logging
import re



def get_cls_name(cls_str: str) -> str:
    __cls_name_search_result = re.search(r"<class '__main__\..[0-32]'>", re.escape(cls_str))
    if __cls_name_search_result is not None:
        cls_name = __cls_name_search_result.group(0)
    else:
        logging.warning(f"Cannot parse strategy class naming and return __class__.")
        cls_name = ""

    return cls_name



class ImportModule:

    __Root_Package = "smoothcrawler"

    @classmethod
    def get_class(cls, pkg_name: str, cls_name: str) -> Callable:
        pkg = import_module(name=pkg_name, package=cls.__Root_Package)
        __class: Callable = getattr(pkg, cls_name)
        return __class

