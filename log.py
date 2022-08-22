import logging

class Log(object):

    def __init__(self) -> None:
        # create logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # create formatter
        formatter = logging.Formatter(fmt="[%(asctime)s] [%(levelname)-0.4s]\t%(message)s",
                                    datefmt="%Y.%m.%d %H:%M:%S")

        # add formatter to ch
        ch.setFormatter(formatter)

        # create file handler
        fileHandler = logging.FileHandler("./log.log")
        fileHandler.setFormatter(formatter)

        # add console and file handlers to logger
        logger.addHandler(ch)
        logger.addHandler(fileHandler)

        logger.info('logger created')
        
        self.logger = logger

        # "application" code
        # logger.debug("debug message")
        # logger.info("info message")
        # logger.warning("warn message")
        # logger.error("error message")
        # logger.critical("critical message")

    def info(self, message :str):
        self.logger.info(message)