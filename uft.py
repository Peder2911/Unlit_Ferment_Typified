import sys
import os

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

from lib import PdfDoc
from lib import LodWriter
from lib import filefuncs
from lib import listfuncs

import json
import itertools

import logging
cl = logging.getLogger('console')

if __name__ == '__main__':

    # argument stuff ###############

    if len(sys.argv) == 1:
        raise Exception('Usage : [pdfpath]')

    if '--dbg' in sys.argv:
        logging.basicConfig(level = 'DEBUG')
    elif '-v' in sys.argv:
        logging.basicConfig(level = 'INFO')

    # dfi compatibility

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

    try:
        outfile = sys.argv[sys.argv.index('-o')+1]
    except (IndexError,ValueError):
        outfile = 'out.csv'

    outfile = os.path.join(mypath,outfile)

    # gather paths and make docs ###

    if os.path.isdir(tgtFolder):
        paths = filefuncs.pdfWalk(tgtFolder)
        pdfs = [PdfDoc.PdfDoc(path) for path in paths] 
    else:
        raise NotADirectoryError('Pdf directory %s not found'%(tgtFolder))

    # get and merge data ###########

    def getData(pdfs,formatPres):
        data = [doc.generalFormat(formatPresPath) for doc in pdfs]
        data = list(itertools.chain.from_iterable(data))
        return(data)

    if len(pdfs) > 10:
        chunks = [*listfuncs.chunk(pdfs,10)]
        cl.info('split into %i chunks'%(len(chunks)))

        data = []

        for n,chnk in enumerate(chunks):
            cl.info('working with chunk %i'%(n))
            data = getData(chnk,formatPresPath)

            if n == 0:
                fmode = 'w'
            else:
                fmode = 'a'

            with open(outfile,fmode) as file:
                Writer = LodWriter.LodWriter(data,file)
                Writer.write()

    else:
        data = [doc.generalFormat(formatPresPath) for doc in pdfs]
        data = list(itertools.chain.from_iterable(data))

        with open('out.csv','w') as file:
            Writer = LodWriter.LodWriter(data,file)
            Writer.write()
