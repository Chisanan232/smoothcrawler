from ._spec import AppIntegrationTestSpec



class TestModuleFactory(AppIntegrationTestSpec):

    def _import_process(self) -> None:
        from smoothcrawler.appintegration.factory import ApplicationIntegrationFactory

