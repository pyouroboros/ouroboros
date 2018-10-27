import logging


def set_logger(level='info'):
    """Set log level (Default=info)"""
    levels = {
        'notset': logging.NOTSET,
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    if level not in levels:
        level = 'info'
    return {'format': '[%(levelname)-s] %(asctime)s %(message)s', 'level': levels.get(level.lower()), 'datefmt': '%Y-%m-%d %H:%M:%S'}
