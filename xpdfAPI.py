#!/usr/bin/env python
import subprocess
import os
import logging

try:
    from . import util
except ImportError:
    import util

cl = logging.getLogger('base_console')

def xpdf(script,file,args = False):
    cl.debug('Running %s on %s'%(script,file))
    call = [util.relPath(script),util.relPath(file)]
    if args:
        call += args

    p = subprocess.run(call,
                       stdout = subprocess.PIPE,
                       stderr = subprocess.PIPE)
    op = p.stdout.decode('utf8','ignore')
    return(op)

def xpdfInfo(file):
    info = xpdf('./lib/xpdf/pdfinfo',file)
    return(info)

def xpdfText(file):
    cl.info('\nReading %s'%(file))
    text = xpdf('./lib/xpdf/pdftotext' ,file ,args = ['-'])
    return(text)
