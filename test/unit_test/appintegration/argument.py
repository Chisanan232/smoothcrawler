from ._spec import AppIntegrationTestSpec



class TestModuleArgument(AppIntegrationTestSpec):

    def _import_process(self) -> None:
        from smoothcrawler.appintegration.argument import BaseMessageQueueArgument, ProducerArgument, ConsumerArgument

