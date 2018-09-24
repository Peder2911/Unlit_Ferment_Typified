#!/usr/bin/env python
import sys
import os

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

import subprocess
import os
import logging

cl = logging.getLogger('console')

def xpdf(script,pdfFile,args = False):
    cl.debug('Running %s on %s'%(script,pdfFile))
    call = os.path.join(mypath,'xpdf',script)
    call = [call,pdfFile]

    if args:
        call += args

    p = subprocess.run(call,
                       stdout = subprocess.PIPE,
                       stderr = subprocess.PIPE)
    op = p.stdout.decode('utf8','ignore')

    return(op)

def info(pdfFile):
    info = xpdf('pdfinfo',pdfFile)
    return(info)

def text(pdfFile):
    text = xpdf('pdftotext',pdfFile,args = '-')
    return(text)
