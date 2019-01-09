from prometheus_client import REGISTRY
import Ouroboros.dataexporters as metrics


def test_container_updates():
    test_label = 'test'
    metrics.container_updates(label=test_label)
    increment = REGISTRY.get_sample_value('containers_updated_total', labels={'container': test_label})
    assert increment == 1.0


def test_monitored_containers():
    test_count = 5.0
    metrics.monitored_containers(num=test_count)
    num_monitored = REGISTRY.get_sample_value('containers_being_monitored')
    assert num_monitored == test_count
