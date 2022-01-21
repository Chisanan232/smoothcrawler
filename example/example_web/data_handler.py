from smoothcrawler.components.data import BaseDataHandler, BaseAsyncDataHandler



class ExampleDataHandler(BaseDataHandler):

    def process(self, result):
        return result



class ExampleAsyncDataHandler(BaseAsyncDataHandler):

    async def process(self, result):
        return result


