from logging import Filter, DEBUG, INFO, WARN, ERROR, CRITICAL, getLogger, Formatter, StreamHandler


class BlacklistFilter(Filter):
    """
    Log filter for blacklisted tokens and passwords
    """

    blacklisted_keys = ['repo_user', 'repo_pass', 'auth_json', 'webhook_urls', 'docker_sockets',
                        'prometheus_exporter_addr', 'influx_username', 'influx_password', 'influx_url']

    def __init__(self, filteredstrings):
        super().__init__()
        self.filtered_strings = filteredstrings

    def filter(self, record):
        for item in self.filtered_strings:
            try:
                if item in record.msg:
                    record.msg = record.msg.replace(item, 8 * '*' + item[-5:])
                if any(item in str(arg) for arg in record.args):
                    record.args = tuple(arg.replace(item, 8 * '*' + item[-5:]) if isinstance(arg, str) else arg
                                        for arg in record.args)
            except TypeError:
                pass
        return True


class OuroborosLogger(object):
    mappings = {
        'debug': DEBUG,
        'info': INFO,
        'warn': WARN,
        'error': ERROR,
        'critical': CRITICAL
    }

    def __init__(self, level=None):
        if level and OuroborosLogger.mappings.get(level):
            self.log_level = OuroborosLogger.mappings.get(level)
        else:
            self.log_level = OuroborosLogger.mappings['info']

        # Create the Logger
        self.logger = getLogger()
        self.logger.setLevel(self.log_level)

        # Create a Formatter for formatting the log messages
        logger_formatter = Formatter('%(asctime)s : %(levelname)s : %(module)s : %(message)s', '%Y-%m-%d %H:%M:%S')

        # Add the console logger
        console_logger = StreamHandler()
        console_logger.setFormatter(logger_formatter)
        console_logger.setLevel(self.log_level)

        # Add the Handler to the Logger
        self.logger.addHandler(console_logger)
