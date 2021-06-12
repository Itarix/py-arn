import logging


class Log:
    """
    Class Log
    """
    logger: logging.Logger or None
    verbose: bool

    def __init__(self, logger: logging.Logger = None, verbose: bool = False, filename: str = ""):
        self.verbose = verbose
        if logger is None:
            logging.basicConfig(filename=filename, filemode='w', level=logging.INFO)
            logger = logging.getLogger(__name__)
        self.logger = logger

    def debug(self, message: str):
        """

        :param message:
        """
        if self.verbose:
            print(message)
        if self.logger is not None:
            self.logger.debug(message)

    def info(self, message: str):
        """

        :param message:
        """
        if self.verbose:
            print(message)
        if self.logger is not None:
            self.logger.info(message)

    def warning(self, message: str):
        """

        :param message:
        """
        if self.verbose:
            print(message)
        if self.logger is not None:
            self.logger.warning(message)

    def error(self, message: str):
        """

        :param message:
        """
        if self.verbose:
            print(message)
        if self.logger is not None:
            self.logger.error(message)
