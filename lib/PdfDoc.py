
import sys
import os

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

import Xpdf
import PresReader

import json
import re

import logging
cl = logging.getLogger('console')

class PdfDoc():
    def __init__(self,pdfFile):
        self.file = pdfFile
    
    def generalFormat(self,formatPres):

        docFormat = PresReader.get(formatPres)
        cl.critical(str(docFormat))

        docs = re.split(docFormat['separator'],Xpdf.text(self.file))

        cl.critical('%i docs'%(len(docs)))

        res = []
        
        for doc in docs:
            doc = re.sub(docFormat['rinse'],' ',doc)
            row = {}
            row['body'] = doc
            
            lead = re.split(docFormat['date'],doc)[0]
            row['headline'] = self.safeRe(docFormat['headline'],lead)

            row['date'] = self.safeRe(docFormat['date'],doc)
            row['source'] = self.safeRe(docFormat['source'],doc)
            res.append(row)
    
        return(res)
    def safeRe(self,pattern,string):
        # Returns first match, if match, otherwise returns NA
        srch = re.search(pattern,string)
        if srch:
            match = srch.group(0)
        else:
            match = 'NA'
        return(match)

    def __str__(self):
        return(Xpdf.text(self.file))
