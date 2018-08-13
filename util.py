import os

def relPath(file):
    dir = os.path.dirname(__file__)
    path = os.path.join(dir,file)
    return(path)
