import sys
import os

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

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
                 [--fp formatPres][--dfi][-v][--dbg][-o outfile][--gf]''')
        sys.exit(1)

    if '--dbg' in sys.argv:
        logging.basicConfig(level = 'DEBUG')
    elif '-v' in sys.argv:
        logging.basicConfig(level = 'INFO')

    if '--gf' in sys.argv:
        chosenFormat = 'generalFormat'
    else:
        chosenFormat = 'fulltext'

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

    # chunk or not #################

    if len(pdfs) > 50:
        chunks = [*listfuncs.chunk(pdfs,10)]
        cl.info('split into %i chunks'%(len(chunks)))

        data = []

        for n,chnk in enumerate(chunks):
            cl.info('working with chunk %i'%(n))

            if chosenFormat == 'generalFormat': 
                data = getData(chnk,formatPresPath)

                if n == 0:
                    fmode = 'w'
                else:
                    fmode = 'a'

                with open(outfile,fmode) as file:
                    Writer = LodWriter.LodWriter(data,file)
                    Writer.write()
                    cl.info('wrote to file')
                    filesize = int(os.stat(outfile).st_size)/1000000
                    cl.info('file currently at %f megabytes'%(filesize))

            else:
                data = {d.filename:str(d) for d in chnk}

                for filename,content in data.items():
                    directory = os.path.dirname(outfile)
                    filename = filename + '.txt'

                    with open(os.path.join(directory,filename),'w') as file:
                        file.write(content)
                    

    # No chunk #####################

    else:
        data = getData(pdfs,formatPresPath)

        with open('out.csv','w') as file:
            try:
                Writer = LodWriter.LodWriter(data,file)
                Writer.write()
            except AttributeError:
                for n,doc in enumerate(data):
                    file.write('{id}{data}'.format(id = n,data = doc))

