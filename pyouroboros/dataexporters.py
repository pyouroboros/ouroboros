from logging import getLogger
import prometheus_client


class DataManager(object):
    def __init__(self, config):
        self.config = config
        self.logger = getLogger()

        self.prometheus_exporter = PrometheusExporter(config) if self.config.prometheus else None
        self.influx = None

    def add(self, label):
        if self.prometheus_exporter:
            self.prometheus_exporter.update(label)

        if self.influx:
            pass

    def set(self, monitored_count):
        if self.prometheus_exporter:
            self.prometheus_exporter.set_monitored(monitored_count)

        if self.influx:
            pass


class PrometheusExporter(object):
    def __init__(self, config):
        self.config = config
        self.http_server = prometheus_client.start_http_server(
            addr=self.config.prometheus_exporter_addr,
            port=self.config.prometheus_exporter_port
        )
        self.updated_containers_counter = prometheus_client.Counter(
            'containers_updated',
            'Count of containers updated',
            ['container']
        )
        self.monitored_containers_gauge = prometheus_client.Gauge(
            'containers_being_monitored',
            'Count of containers being monitored',
            []
        )
        self.logger = getLogger()

    def set_monitored(self, count):
        """Set number of containers being monitoring with a gauge"""
        self.monitored_containers_gauge.set(count)
        self.logger.debug("Prometheus Exporter monitored containers gauge set to %s", count)

    def update(self, label):
        """Increment container update count based on label"""
        self.updated_containers_counter.labels(container=label).inc()
        self.logger.debug("Prometheus Exporter container update counter incremented for %s", label)
