from prometheus_client import Counter, Gauge

updated_containers_counter = Counter(
    'containers_updated', 'Count of containers updated', ['container'])

monitored_containers_gauge = Gauge(
    'containers_being_monitored', 'Count of containers being monitored', [])


def container_updates(label):
    """Increment container update count based on label"""
    updated_containers_counter.labels(container=label).inc()


def monitored_containers(num):
    """Set number of containers being monitoring with a gauge"""
    monitored_containers_gauge.set(num)
