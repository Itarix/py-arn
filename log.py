import logging

def format_error(error_message, val1, val2, index):
    return f'Error: {error_message:30} => sequence 1 : {val1:1} vs sequence 2 : {val2:1} ==> at position {index:10d}'

class Log:
    logger: logging.Logger

    def __init__(self, logger:logging.Logger=None, verbose:bool=False, filename:str=""):
        self.verbose = verbose
        self.logger = logger
        if logger is None:
            self.logger = logging.basicConfig(filename=filename, encoding='utf-8', level=logging.DEBUG)

    def debug(self, message:str):
        if self.verbose:
            print(message)
        if self.logger is not None:
            self.logger.debug(message)

    def info(self, message:str):
        if self.verbose:
            print(message)
        if self.logger is not None:
            self.logger.info(message)

    def warning(self, message:str):
        if self.verbose:
            print(message)
        if self.logger is not None:
            self.logger.warning(message)

    def error(self, message:str):
        if self.verbose:
            print(message)
        if self.logger is not None:
            self.logger.error(message)
