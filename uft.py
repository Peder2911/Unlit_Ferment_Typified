import sys
import os

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

from lib import PdfDoc

import json
import itertools

import logging

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
    if len(sys.argv) == 1:
        raise Exception('Usage : [pdfpath]')

    if '-d' in sys.argv:
        logging.basicConfig(level = 0)

    if '--dfi' in sys.argv:
        config = json.load(sys.stdin)
        tgtFolder = config['pdf folder']

        rconf = config['redis']
        r = redis.Redis(host = rconf['hostname'],
                        port = rconf['port'],
                        db = rconf['db'])
    else:
        tgtFolder = sys.argv[1]

    try:
        formatPresPath = sys.argv[sys.argv.index('--fp')+1]
    except (IndexError,ValueError):
        formatPresPath = 'data/defaultformat.pres'
    
    formatPresPath = os.path.join(mypath,formatPresPath)

    if os.path.isdir(tgtFolder):
        pdfs = [PdfDoc.PdfDoc(d) for d in pdfWalk(tgtFolder)]
    else:
        raise NotADirectoryError('Pdf directory %s not found'%(tgtFolder))

    data = [doc.generalFormat(formatPresPath) for doc in pdfs]
    for entry in data:
        for sentry in entry:
            print(sentry['date'])
            print(sentry['source'])
            print(sentry['body'][:20])
