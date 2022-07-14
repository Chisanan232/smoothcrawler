from ._spec import AppIntegrationTestSpec



class TestModuleCrawler(AppIntegrationTestSpec):

    def _import_process(self) -> None:
        from smoothcrawler.appintegration.__pkg_info__ import (
            __title__,
            __version__,
            __description__,
            __license__,
            __author__,
            __author_email__,
            __copyright__,
            __url__
        )

