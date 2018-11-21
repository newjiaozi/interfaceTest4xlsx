#coding=utf-8

import logging
from logging import handlers
import os

def __get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.INFO)
    handler = handlers.TimedRotatingFileHandler(filename="..%slogs%slog.txt" % (os.sep,os.sep),when="D")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.INFO)
    if handler not in logger.handlers:
        logger.addHandler(handler)
    if console not in logger.handlers:
        logger.addHandler(console)
    return logger

logger = __get_logger("interfaceTest")