import pytest
import ouroboros.logger as log

@pytest.mark.parametrize('level_string, level_code', [
    ('debug', 10),
    ('info', 20),
    ('warn', 30),
    ('error', 40),
    ('critical', 50),
])

def test_logger_levels(level_string, level_code):
    assert log.set_logger(level_string)['level'] == level_code

def test_logger_invalid_level():
    assert log.set_logger('wrong')['level'] == 20