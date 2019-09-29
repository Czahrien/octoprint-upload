#!/usr/bin/env python3
import settings
import requests
import os
import sys
import time
import glob

import logging

# Initialize the logger
FORMAT = "%(asctime)s %(levelname)s-(%(filename)s:%(lineno)d)-%(message)s"
logger = logging.getLogger("uploadGCode")
format = logging.Formatter(FORMAT)
sh = logging.StreamHandler()
sh.setFormatter(fmt=format)
fh = logging.FileHandler('upload.log')
fh.setFormatter(fmt=format)
logger.addHandler(sh)
logger.addHandler(fh)
logger.setLevel(logging.INFO)

# OctoPrint uses an API key in the request header to authenticate
header = {'X-Api-Key': settings.apiKey}

def main():
    try:
        os.mkdir(settings.doneFilePath)
    except:
        pass

    # Find files in the current working directory with a .gcode extension
    files = glob.glob("*.gcode")
    logger.info("Files: %s" % files)

    for file in files:
        if False == processFile(file):
            return 1
    return 0

def processFile(file):
    logger.info("Uploading %s..." % file)
    # Post the file to the configured URL
    try:
        r = requests.post(settings.url, headers=header, files={
            'file': (settings.uploadFilePath + '/' + file, open(file, 'rb'))
        })
        if(r.ok):
            # Successful transfer - move to the done directory to get it out of this directory.
            os.rename(file, settings.doneFilePath + '/' + file)
            return True
        else:
            logger.error(r)
            logger.error(r.text)
    except Exception as e:
        logger.error(e)
    return False

if __name__ == '__main__':
    retval = main()
    logger.info('main returned %d' % retval)
    time.sleep(5)
    sys.exit(retval)
