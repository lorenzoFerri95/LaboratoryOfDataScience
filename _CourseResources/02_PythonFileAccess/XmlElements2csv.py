# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 01:32:54 2018

@author: Anna
"""
import sys, getopt
import xml.etree.ElementTree as ET

def getAttributes(root):
    attNames = set()
    for row in root:
        for att in row:
            attNames.add(att.tag)
    return attNames

# Store input and output file names
ifile=''
ofile=''
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"i:o:")
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-i':
        ifile=a
    elif o == '-o':
        ofile=a
    else:
        print("Usage: %s -i input -o output /n" % sys.argv[0])

# open XML
d = ET.parse(ifile)
root = d.getroot()
nrows = len(root)
first = True
if nrows == 0:
    print("This file does not contain any row")
else:
    attNames = getAttributes(root)
    #Output metadata
    fileOut = open(ofile,"w")
    for attn in attNames:
        if first:
            first = False
        else:
            fileOut.write(",")
        fileOut.write(attn)
        
fileOut.write("\n");
#output data
for row in root:
    first = True;
    for attn in attNames:
        if first:
            first = False
        else:
            fileOut.write(",")
        att = row.find(attn)
        if att is None: 
            fileOut.write("?")
        else:
            fileOut.write(att.text);
    fileOut.write("\n");
fileOut.close()

   