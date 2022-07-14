from ._spec import AppIntegrationTestSpec



class TestModuleRole(AppIntegrationTestSpec):

    def _import_process(self) -> None:
        from smoothcrawler.appintegration.role import CrawlerSource, CrawlerProducer, CrawlerProcessor, CrawlerConsumer

