#!/usr/bin/env python

import os
import sys

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

import redis

import itertools

import logging
from logging.config import dictConfig

import json
import yaml

####################################
# What is this even

try:
    from . import apiEmu
except ImportError:
    import apiEmu

try:
    from . import util
except ImportError:
    import util

####################################

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

    # Argument stuff, ##############
    # Replaced by new dfi scheme ###
#
#    tgtFolder = sys.argv[1]
#    outFile = sys.argv[2]
#    if outFile == 'stdout':
#        outFile = sys.stdout
#
#    if '-d' in sys.argv:
#        cl.setLevel('DEBUG')
#    elif '-i' in sys.argv:
#        cl.setLevel('INFO')
#    else:
#        cl.setLevel('WARNING')
#
    ################################

    cl = logging.getLogger('console')

    config = json.load(sys.stdin)
    tgtFolder = config['pdf folder']

    rconf = config['redis']
    r = redis.Redis(host = rconf['hostname'],
                    port = rconf['port'],
                    db = rconf['db'])
    

    if os.path.isdir(tgtFolder):
        pdfs = pdfWalk(tgtFolder)
    else:
        raise NotADirectoryError('Pdf directory %s not found'%(tgtFolder))

    formatted = [apiEmu.pdfToFormatted(f) for f in pdfs]

    for formatted_pdf in formatted:
        r.lpush('data',formatted_pdf)

#    outFile = sys.stdout
#
#    if outFile is not sys.stdout:
#        cl.debug('Writing %i docs to %s'%(len(formatted),outFile))
#        with open(outFile,'w') as file:
#            json.dump(formatted,file)
#    else:
#        jsonText = json.dumps(formatted)
#        sys.stdout.write(jsonText)
