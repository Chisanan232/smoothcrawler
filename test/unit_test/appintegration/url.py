from ._spec import AppIntegrationTestSpec



class TestModuleURL(AppIntegrationTestSpec):

    def _import_process(self) -> None:
        from smoothcrawler.appintegration.url import FileBasedURL, MessageQueueURLProducer

