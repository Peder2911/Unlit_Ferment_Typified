import os
import itertools
import logging

cl = logging.getLogger('console')

def pdfWalk(folder):
    def listFiles(directory,type = 'pdf'):
        dir = directory[0]
        files = directory[2]
        folderPaths = [os.path.join(dir,f) for f in files if f[-3:] == type]
        folderPaths = [os.path.abspath(f) for f in folderPaths]
        return(folderPaths)

    allPaths = [listFiles(dir) for dir in os.walk(folder)]
    allPaths = list(itertools.chain.from_iterable(allPaths))

    cl.info('found %i files'%(len(allPaths)))

    return(allPaths)

