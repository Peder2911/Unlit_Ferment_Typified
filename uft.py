import sys
import os
import json

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

import boltons.iterutils
import itertools

from lib import PdfDoc
from lib import filefuncs

from dfitools.RedisDf import RedisDf
import redis

import colorama

import logging
cl = logging.getLogger('console')

if __name__ == '__main__':
    # setup ########################
    colorama.init(autoreset = True)

    chosenFormat = 'generalFormat'
    presPath = os.path.join(mypath,'data/defaultformat.pres')


    config = json.load(sys.stdin)
    rconf = config['redis']
    tgtFolder = config['pdf folder']

    rdf = RedisDf(host = rconf['hostname'],
                  port = rconf['port'],
                  db = rconf['db'],
                  key = rconf['listkey'])

    # gather paths and make docs ###
    if os.path.isdir(tgtFolder):
        paths = filefuncs.pdfWalk(tgtFolder)
        pdfs = [PdfDoc.PdfDoc(path) for path in paths] 
    else:
        raise NotADirectoryError('Pdf directory %s not found'%(tgtFolder))

    if len(pdfs) > config['chunksize']/100:
        npdf = len(pdfs)
        pdfs = boltons.iterutils.chunked(pdfs,int(config['chunksize'] / 100))
        nch = len(pdfs)
        print(colorama.Fore.YELLOW + '%i pdfs in %i chunks'%(npdf,nch))
    else:
        pdfs = [pdfs]
   
    for i,ch in enumerate(pdfs):
        print(colorama.Fore.YELLOW + 'Chunk %i'%(i+1))
        data = [doc.generalFormat(presPath) for doc in ch]
        data = list(itertools.chain.from_iterable(data))
        print(colorama.Fore.BLUE + '%i docs' %(len(data)))
        rdf.writeChunk(data)

    rdf.commit()
