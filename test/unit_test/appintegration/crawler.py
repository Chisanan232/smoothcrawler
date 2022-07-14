from ._spec import AppIntegrationTestSpec



class TestModuleCrawler(AppIntegrationTestSpec):

    def _import_process(self) -> None:
        from smoothcrawler.appintegration.crawler import FileBasedCrawler, MessageQueueCrawler

