import prometheus_client

from logging import getLogger
from influxdb import InfluxDBClient
from datetime import datetime, timezone


class DataManager(object):
    def __init__(self, config):
        self.config = config
        self.logger = getLogger()
        self.enabled = True

        self.monitored_containers = {}
        self.total_updated = {}

        self.prometheus = PrometheusExporter(self, config) if self.config.data_export == "prometheus" else None
        self.influx = InfluxClient(self, config) if self.config.data_export == "influxdb" else None

    def add(self, label, socket):
        if self.config.data_export == "prometheus" and self.enabled:
            self.prometheus.update(label, socket)

        elif self.config.data_export == "influxdb" and self.enabled:
            if label == "all":
                self.logger.debug("Total containers updated %s", self.total_updated[socket])

            self.influx.write_points(label, socket)

    def set(self, socket):
        if self.config.data_export == "prometheus" and self.enabled:
            self.prometheus.set_monitored(socket)


class PrometheusExporter(object):
    def __init__(self, data_manager, config):
        self.config = config
        self.data_manager = data_manager
        self.http_server = prometheus_client.start_http_server(
            self.config.prometheus_port,
            addr=self.config.prometheus_addr
        )
        self.updated_containers_counter = prometheus_client.Counter(
            'containers_updated',
            'Count of containers updated',
            ['socket', 'container']
        )
        self.monitored_containers_gauge = prometheus_client.Gauge(
            'containers_being_monitored',
            'Gauge of containers being monitored',
            ['socket']
        )
        self.updated_all_containers_gauge = prometheus_client.Gauge(
            'all_containers_updated',
            'Count of total updated',
            ['socket']
        )
        self.logger = getLogger()

    def set_monitored(self, socket):
        """Set number of containers being monitoring with a gauge"""
        self.monitored_containers_gauge.labels(socket=socket).set(self.data_manager.monitored_containers[socket])
        self.logger.debug("Prometheus Exporter monitored containers gauge set to %s",
                          self.data_manager.monitored_containers[socket])

    def update(self, label, socket):
        """Set container update count based on label"""
        if label == "all":
            self.updated_all_containers_gauge.labels(socket=socket).set(self.data_manager.total_updated[socket])
        else:
            self.updated_containers_counter.labels(socket=socket, container=label).inc()

        self.logger.debug("Prometheus Exporter container update counter incremented for %s", label)


class InfluxClient(object):
    def __init__(self, data_manger, config):
        self.data_manager = data_manger
        self.config = config
        self.logger = getLogger()
        self.influx = InfluxDBClient(
            host=self.config.influx_url,
            port=self.config.influx_port,
            username=self.config.influx_username,
            password=self.config.influx_password,
            database=self.config.influx_database,
            ssl=self.config.influx_ssl,
            verify_ssl=self.config.influx_verify_ssl
        )
        self.db_check()

    def db_check(self):
        database_dicts = self.influx.get_list_database()
        databases = [d['name'] for d in database_dicts]
        if self.config.influx_database in databases:
            self.logger.debug("Influxdb database existence check passed for %s", self.config.influx_database)
        else:
            self.logger.debug("Influxdb database existence failed for %s. Disabling exports.",
                              self.config.influx_database)
            self.data_manager.enabled = False

    def write_points(self, label, socket):
        clean_socket = socket.split("//")[1]
        now = datetime.now(timezone.utc).astimezone().isoformat()
        influx_payload = [
            {
                "measurement": "Ouroboros",
                "tags": {'socket': clean_socket},
                "time": now,
                "fields": {}
            },
            {
                "measurement": "Ouroboros",
                "tags": {'configuration': self.config.hostname},
                "time": now,
                "fields": {key: (value if not isinstance(value, list) else ' '.join(value)) for key, value in
                           vars(self.config).items() if key.upper() in self.config.options}
            }
        ]
        if label == "all":
            influx_payload[0]['tags']["type"] = "stats"
            influx_payload[0]['fields'] = {
                "monitored_containers": self.data_manager.monitored_containers[socket],
                "updated_count": self.data_manager.total_updated[socket]
            }
        else:
            influx_payload[0]['tags'].update(
                {
                    "type": "container_update",
                    "container": label
                }
            )
            influx_payload[0]['fields'] = {"count": 1}

        self.logger.debug("Writing data to influxdb: %s", influx_payload)
        self.influx.write_points(influx_payload)
