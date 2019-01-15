from logging import Filter, getLogger, Formatter, StreamHandler


class BlacklistFilter(Filter):
    """
    Log filter for blacklisted tokens and passwords
    """

    blacklisted_keys = ['repo_user', 'repo_pass', 'auth_json', 'webhook_urls', 'docker_sockets', 'pushover_user',
                        'prometheus_addr', 'influx_username', 'influx_password', 'influx_url', 'pushover_token',
                        'pushover_devices', 'smtp_host', 'smtp_username', 'smtp_password', 'smtp_recipients',
                        'smtp_from_email']

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
    def __init__(self, level='INFO'):
        # Create the Logger
        self.logger = getLogger()
        try:
            self.logger.setLevel(level.upper())
        except ValueError:
            level = "INFO"
            self.logger.setLevel(level.upper())

        # Create a Formatter for formatting the log messages
        logger_formatter = Formatter('%(asctime)s : %(levelname)s : %(module)s : %(message)s', '%Y-%m-%d %H:%M:%S')

        # Add the console logger
        console_logger = StreamHandler()
        console_logger.setFormatter(logger_formatter)

        console_logger.setLevel(level.upper())

        # Add the Handler to the Logger
        self.logger.addHandler(console_logger)
