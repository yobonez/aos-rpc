import logging
import logging.handlers
import datetime
import sys
import os
import zipfile

try:
    files = os.listdir("logs/")
except FileNotFoundError:
    os.mkdir("logs/")
    files = os.listdir("logs/")
    
for file_name in files:
    file_name_new = 'logs/' + file_name

    log_to_zip = file_name.replace(".log", ".zip")

    if file_name_new.find('.zip') == -1:
        with zipfile.ZipFile("logs/" + log_to_zip, 'w', compresslevel=9, compression=zipfile.ZIP_DEFLATED) as log_zip:
            log_zip.write(file_name_new)
            try:
                os.remove(file_name_new)
            except PermissionError:
                pass

now = datetime.datetime.now()
timestamp = str(now.strftime("%Y_%m_%d_%H-%M-%S"))

def uncaught_exception(excepttype, value, tb):
    logger.critical("Uncaught exception: ", exc_info=(excepttype, value, tb))
sys.excepthook = uncaught_exception

logger = logging.getLogger('aos-rpc')
logger.setLevel(logging.DEBUG)

if os.path.isdir('./logs'):
    fileHandler = logging.handlers.RotatingFileHandler(filename='./logs/{} aos-rpc.log'.format(timestamp),
                                                       encoding='utf-8')
else:
    os.mkdir('./logs')
    fileHandler = logging.handlers.RotatingFileHandler(filename='./logs/{} aos-rpc.log'.format(timestamp),
                                                       encoding='utf-8')
fileHandler.setLevel(logging.DEBUG)

streamHandler = logging.StreamHandler(stream=sys.stdout)
streamHandler.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)
