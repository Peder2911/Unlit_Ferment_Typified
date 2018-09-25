
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
        self.filename = os.path.split(self.file)[1]

    def generalFormat(self,formatPres):
        # Extracts date, headline, body and source from document using a .pres file
        # containing several regexi.

        # The procedure is like this:
        # First finds the date, which validates the document
        # If there is a date, split the doc into a lead and bod section using
        # the slseparator, making it easier to extract the source and hl strings.
        # These are then extracted using regexi
        # The body is simply the entire "bod" section, which is probably pretty noisy.
        # Sentence extraction from these documents must include some cleaning, and / or
        # validation of sentences.

        docFormat = PresReader.get(formatPres)

        docs = re.split(docFormat['separator'],Xpdf.text(self.file))
        docs.pop()

        cl.info('%i docs in %s'%(len(docs),self.filename))

        res = []
        
        for doc in docs:

            doc = re.sub(docFormat['rinse'],' ',doc)
            row = {}
            
            row['date'] = self.safeRe(docFormat['date'],doc)
            
            row['filename'] = self.filename 

            if row['date'] != 'NA':

                splitdoc = re.split(docFormat['slseparator'],doc)
                splitdoc = [d for d in splitdoc if d is not None]

                if len(splitdoc) >= 2:
                    lead = splitdoc[0]
                    bod = splitdoc[1]
                
                    row['body'] = bod.strip() 
                    row['headline'] = lead.strip()
                    row['source'] = self.safeRe(docFormat['source'],bod)

                else:
                    row['body'] = 'NA'
                    row['source'] = 'NA'
                    row['headline'] = 'NA'
            else:
                row['body'] = 'NA'
                row['source'] = 'NA'
                row['headline'] = 'NA'

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
