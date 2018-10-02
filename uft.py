import sys
import os

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

import io

from lib import PdfDoc
from lib import LodWriter

from lib import filefuncs
from lib import listfuncs

import csv
import json
import itertools

import logging
cl = logging.getLogger('console')

if __name__ == '__main__':

    # argument stuff ###############

    if len(sys.argv) == 1:
        print('''Usage : python3 uft.py pdf_directory 
                 [--fp formatPres][--dfi][-v][--dbg][-o outFile][--gf]''')
        sys.exit(1)

    if '--dbg' in sys.argv:
        logging.basicConfig(level = 'DEBUG')
    elif '-v' in sys.argv:
        logging.basicConfig(level = 'INFO')

    if '--gf' in sys.argv:
        chosenFormat = 'generalFormat'

        try:
            presPath = sys.argv[sys.argv.index('--fp')+1]
        except (IndexError,ValueError):
            presPath = 'data/defaultformat.pres'

        presPath = os.path.join(mypath,presPath)

    else:
        chosenFormat = 'fulltext'
        presPath = None

    if '--dfi' in sys.argv:
        # dfi compatibility
        import redis
        from dfitools import RedisFile

        config = json.load(sys.stdin)
        # print(json.dumps(config))
        tgtFolder = config['pdf folder']

        rconf = config['redis']
        outFile = RedisFile.RedisFile(listkey = rconf['listkey'],
                                      host = rconf['hostname'],
                                      port = rconf['port'],
                                      db = rconf['db'])
    else:
        tgtFolder = sys.argv[1]
        try:
            outFile = sys.argv[sys.argv.index('-o')+1]
        except (IndexError,ValueError):
            outFile = 'out.csv'
        outFile = os.path.join(mypath,outFile)
        open(outFile,'w').close()
        outFile = open(outFile,'a')

    # gather paths and make docs ###

    if os.path.isdir(tgtFolder):
        paths = filefuncs.pdfWalk(tgtFolder)
        pdfs = [PdfDoc.PdfDoc(path) for path in paths] 
    else:
        raise NotADirectoryError('Pdf directory %s not found'%(tgtFolder))

    # get and merge data ###########

    def getData(pdfs,dataFormat = None, pres = None):
        # Gets data from multiple PdfDoc objects
        # data is either retrieved as General Format (genf) data,
        # or in simple string format
        # returns data in a single, flat list.


        if dataFormat == 'generalFormat':
            data = [doc.generalFormat(pres) for doc in pdfs]
            data = list(itertools.chain.from_iterable(data))

            fauxfile = io.StringIO()
            Writer = LodWriter.LodWriter(data,fauxfile)
            Writer.write()
            data = fauxfile.getvalue()
            del(fauxfile)

            # data = json.dumps(data)
        else:
            data = [str(pdf) for pdf in pdfs]
            data = [d.replace('\n',' ') for d in data]
            data = '\n'.join(data)


        return(data)

    if len(pdfs) > 50:
        chunks = [*listfuncs.chunk(pdfs,10)]
        cl.info('split into %i chunks'%(len(chunks)))

        for n,chnk in enumerate(chunks):
            cl.info('working with chunk %i'%(n))
            data = getData(chnk,dataFormat = chosenFormat,pres = presPath) 
            outFile.write(data)

    else:
        data = getData(pdfs,dataFormat = chosenFormat,pres = presPath)
        outFile.write(data)

    outFile.close()
    
