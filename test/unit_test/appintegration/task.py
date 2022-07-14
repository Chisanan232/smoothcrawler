from ._spec import AppIntegrationTestSpec



class TestModuleTask(AppIntegrationTestSpec):

    def _import_process(self) -> None:
        from smoothcrawler.appintegration.task import (
            CSVTask, XLSXTask, JSONTask, XMLTask, PropertiesTask,
            PipeTask, SocketTask,
            SharedDatabaseTask
        )

        from smoothcrawler.appintegration.task import _has_kafka_pkg, _has_pika_pkg, _has_stomp_pkg

        if _has_kafka_pkg():
            from smoothcrawler.appintegration.task import (
                KafkaConfig, KafkaTask
            )

        if _has_pika_pkg():
            from smoothcrawler.appintegration.task import (
                RabbitMQConfig, RabbitMQTask
            )

        if _has_stomp_pkg():
            from smoothcrawler.appintegration.task import (
                ActiveMQConfig, ActiveMQTask
            )

