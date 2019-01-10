import prometheus_client

from logging import getLogger
from influxdb import InfluxDBClient
from datetime import datetime, timezone


class DataManager(object):
    def __init__(self, config):
        self.config = config
        self.logger = getLogger()

        self.prometheus_exporter = PrometheusExporter(config) if self.config.data_export == "prometheus" else None
        self.influx = InfluxClient(config) if self.config.data_export == "influxdb" else None

    def add(self, label):
        if self.config.data_export == "prometheus":
            self.prometheus_exporter.update(label)

        elif self.config.data_export == "influxdb":
            if label == "all":
                self.influx.total_updated += 1
            else:
                self.influx.write_points(label)

    def set(self, monitored_count):
        if self.config.data_export == "prometheus":
            self.prometheus_exporter.set_monitored(monitored_count)

        elif self.config.data_export == "influxdb":
            self.influx.monitored_containers = monitored_count


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


class InfluxClient(object):
    def __init__(self, config):
        self.config = config
        self.influx = InfluxDBClient(
            self.config.influx_url,
            self.config.influx_port,
            self.config.influx_username,
            self.config.influx_password,
            self.config.influx_database
        )

        self.monitored_containers = 0
        self.total_updated = 0

    def write_points(self, label):
        now = datetime.now(timezone.utc).astimezone().isoformat()
        influx_payload = [
            {
                "measurement": "Ouroboros",
                "tags": {
                    "type": "container_update",
                    "container": label
                },
                "time": now,
                "fields": {
                    "count": 1
                }
            }
        ]
        self.influx.write_points(influx_payload)
