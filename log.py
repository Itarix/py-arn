import logging


def format_error(error_message, val1, val2, index):
    return f'Error: {error_message:30} => sequence 1 : {val1:1} vs sequence 2 : {val2:1} ==> at position {index:10d}'


class Log:
    logger: logging.Logger or None
    verbose: bool

    def __init__(self, logger: logging.Logger = None, verbose: bool = False, filename: str = ""):
        self.verbose = verbose
        if logger is None:
            logging.basicConfig(filename=filename, filemode='w', level=logging.INFO)
            logger = logging.getLogger(__name__)
        self.logger = logger

    def debug(self, message: str):
        if self.verbose:
            print(message)
        if self.logger is not None:
            self.logger.debug(message)

    def info(self, message: str):
        if self.verbose:
            print(message)
        if self.logger is not None:
            self.logger.info(message)

    def warning(self, message: str):
        if self.verbose:
            print(message)
        if self.logger is not None:
            self.logger.warning(message)

    def error(self, message: str):
        if self.verbose:
            print(message)
        if self.logger is not None:
            self.logger.error(message)
