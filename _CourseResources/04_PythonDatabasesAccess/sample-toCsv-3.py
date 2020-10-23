# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 23:48:50 2018

@author: Anna
"""

# questo programma esegue una query sul DB e poi scrive i risultati riga per riga in un file CSV.

from datetime import timedelta
import pyodbc
import csv


def toCsvHeader(query_cursor, file_writer):
    file_writer.writerow([x[0] for x in query_cursor.description])  # column headers
    for row in query_cursor:
        file_writer.writerow(row)

def toCsv(query_cursor, file_writer):
    for row in query_cursor:
        file_writer.writerow(row)
        
#connect to data source, using userName and userPWD
server = 'tcp:apa.di.unipi.it' 
database = 'pubs' 
username = 'lds' 
password = 'pisa' 
outfile = 'output.csv'
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()

query="SELECT title, price FROM titles"
cursor.execute(query)

csvfile = open(outfile, 'w', newline='')
writer = csv.writer(csvfile)

toCsv(cursor,writer)
cursor.close()
cnxn.close()
csvfile.close()