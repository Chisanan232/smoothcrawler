from ._spec import AppIntegrationTestSpec



class TestModuleComponents(AppIntegrationTestSpec):

    def _import_process(self) -> None:
        from smoothcrawler.appintegration.components import DataHandlerBeforeBack

