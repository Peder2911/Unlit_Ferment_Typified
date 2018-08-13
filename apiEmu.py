
import re
import json
import logging

import os

try:
    from . import xpdfAPI
except ImportError:
    import xpdfAPI

try:
    from . import util
except ImportError:
    import util

cl = logging.getLogger('base_console')

#####################################

def pdfToFormatted(file):
    text = xpdfAPI.xpdfText(file)
    text = treatText(text)

    formatted = {'date':getDate(text)
                ,'headline':getHeadline(text)
                ,'body':getBody(text)
                ,'source':getSource(file)
                ,'id':getID(text)}

    return(formatted)

#####################################

def getDate(text):
    return('NA')

def getHeadline(text):
    m = re.search('[0-9]+ words',text)
    if m:
        hl = text[:m.start()]
    else:
        hl = text.split('\n')[0]
    return(text.split('\n')[0])

def getBody(text):
    return(text)

def getSource(file):
    return(os.path.basename(file))

def getID(text):
    return('NA')

#####################################

def treatText(text):
    configFile = './data/treatment.json'

    if os.path.isfile(configFile):
        with open(util.relPath(configFile)) as tFile:
            treatmentConfig = json.load(tFile)
    else:
        treatmentConfig = None
        cl.warning('Not processing text: ./data/treatment.json not found')

    if treatmentConfig is not None:
        for regexp in treatmentConfig['purge']:
            cl.info('Purging all %s:'%(repr(regexp)))
            m = re.findall(regexp,text)
            for match in m:
                cl.debug('Removing %s'%(repr(match)))
                text.replace(match,' ')
    else:
        pass

    return(text)
