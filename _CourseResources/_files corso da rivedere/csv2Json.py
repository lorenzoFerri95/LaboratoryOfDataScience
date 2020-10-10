# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 12:48:37 2018

@author: Anna
"""

import sys, getopt
import csv
import json

#Read CSV File
def read_csv(file, json_file, format):
    csv_rows = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
        write_json(csv_rows, json_file, format)

#Convert csv data into json and write it
def write_json(data, json_file, format):
    with open(json_file, "w") as f:
        if format == "pretty":
            f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': ')))
        else:
            f.write(json.dumps(data))


#Get Command Line Arguments

input_file = ''
output_file = ''
format = ''

try:
    opts, args = getopt.getopt(sys.argv[1:],"i:o:f:")
except getopt.GetoptError:
    print ('Usage: csv_json.py -i <path to inputfile> -o <path to outputfile> -f <dump/pretty>')

if len(opts) < 3:
    print ('Usage: csv_json.py -i <path to inputfile> -o <path to outputfile> -f <dump/pretty>')
    sys.exit()

for opt, arg in opts:
    if opt in ("-i", "--ifile"):
        print(arg)
        input_file = arg
    elif opt in ("-o", "--ofile"):
        output_file = arg
        print(arg)
    elif opt in ("-f", "--format"):
        format = arg
        print(arg)
        
read_csv(input_file, output_file, format)

