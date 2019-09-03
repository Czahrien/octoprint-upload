#!/usr/bin/env python3
import settings
import requests
import os
from glob import glob

# OctoPrint uses an API key in the request header to authenticate
header = {'X-Api-Key': settings.apiKey}

try:
    os.mkdir(settings.doneFilePath)
except:
    None

for file in glob("*.gcode"):
    r = requests.post(settings.url, headers=header, files={
        'file': (settings.uploadFilePath + '/' + file, open(file, 'rb'))
    })
    if(r.ok):
        os.rename(file, settings.doneFilePath + '/' + file)
    else:
        print(r)