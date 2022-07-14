from abc import ABCMeta, ABC, abstractmethod

_Has_AppIntegration_Pkg: bool = False

try:
    import smoothcrawler_appintegration
except ImportError:
    _Has_AppIntegration_Pkg = False
else:
    _Has_AppIntegration_Pkg = True



class _BaseAppIntegrationTestSpec(metaclass=ABCMeta):

    @abstractmethod
    def test_import(self) -> None:
        pass


    @abstractmethod
    def _has_smoothcrawler_appintegration_package(self) -> bool:
        pass


    @abstractmethod
    def _import_process(self) -> None:
        pass



class AppIntegrationTestSpec(_BaseAppIntegrationTestSpec, ABC):

    def test_import(self) -> None:
        _Import_Pkg: bool

        try:
            self._import_process()
        except ImportError:
            _Import_Pkg = False
        else:
            _Import_Pkg = True

        assert _Import_Pkg == self._has_smoothcrawler_appintegration_package(), \
            "The importing result should be same as import smoothcrawler_appintegration."


    def _has_smoothcrawler_appintegration_package(self) -> bool:
        global _Has_AppIntegration_Pkg
        return _Has_AppIntegration_Pkg
