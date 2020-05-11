import logging
import logging.handlers
import datetime
import sys
import os

now = datetime.datetime.now()
timestamp = str(now.strftime("%Y_%m_%d_%H-%M-%S"))

def uncaught_exception(excepttype, value, tb):
    logger.critical("Uncaught exception: ", exc_info=(excepttype, value, tb))
sys.excepthook = uncaught_exception

logger = logging.getLogger('aos-presence')
logger.setLevel(logging.DEBUG)

try:
    fileHandler = logging.handlers.RotatingFileHandler(filename='./logs/{} aos-presence.log'.format(timestamp),
                                                       encoding='utf-8')
except FileNotFoundError:
    os.mkdir('./logs')
    fileHandler = logging.handlers.RotatingFileHandler(filename='./logs/{} aos-presence.log'.format(timestamp),
                                                       encoding='utf-8')
fileHandler.setLevel(logging.DEBUG)

streamHandler = logging.StreamHandler(stream=sys.stdout)
streamHandler.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)