#!/usr/bin/env python

import os
import sys
import itertools

import logging
from logging.config import dictConfig

import json
import yaml

try:
    from . import apiEmu
except ImportError:
    import apiEmu

try:
    from . import util
except ImportError:
    import util

def pdfWalk(folder):
    def listFiles(directory,type = 'pdf'):
        dir = directory[0]
        files = directory[2]
        folderPaths = [os.path.join(dir,f) for f in files if f[-3:] == type]
        folderPaths = [os.path.abspath(f) for f in folderPaths]
        return(folderPaths)

    allPaths = [listFiles(dir) for dir in os.walk(folder)]
    allPaths = list(itertools.chain.from_iterable(allPaths))
    return(allPaths)

if __name__ == '__main__':
    with open(util.relPath('data/logging.yaml')) as file:
        logConf = yaml.load(file)

    dictConfig(logConf)

    cl = logging.getLogger('base_console')

    tgtFolder = sys.argv[1]
    outFile = sys.argv[2]
    if outFile == 'stdout':
        outFile = sys.stdout

    if '-d' in sys.argv:
        cl.setLevel('DEBUG')
    elif '-i' in sys.argv:
        cl.setLevel('INFO')
    else:
        cl.setLevel('WARNING')

    pdfs = pdfWalk(tgtFolder)
    formatted = [apiEmu.pdfToFormatted(f) for f in pdfs]

    if outFile is not sys.stdout:
        cl.debug('Writing %i docs to %s'%(len(formatted),outFile))
        with open(outFile,'w') as file:
            json.dump(formatted,file)
    else:
        jsonText = json.dumps(formatted)
        sys.stdout.write(jsonText)
