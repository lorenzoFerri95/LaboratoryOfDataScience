# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 18:01:46 2018

@author: Anna
"""

import pyodbc
import csv

PERCENTAGE=0.30;
tableStrat= 'census'
columnStrat='sex'
outputFile= 'selection.csv' 
csvfile = open(outputFile, 'w', newline='')
writer = csv.writer(csvfile)

#connect to data source, using userName and userPWD
server = 'tcp:apa.di.unipi.it' 
database = 'lbi' 
username = 'lbi' 
password = 'pisa' 
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)
cnxnInn = pyodbc.connect(connectionString)

cursor = cnxn.cursor()
query = "SELECT " + columnStrat + ", COUNT(*)" + " FROM " + tableStrat + " GROUP BY " + columnStrat
cursor.execute(query)          
#scan result of the query to capture the distribution of records wrt the columnStrat
first = True
for row in cursor:
    colValue = row[0]
    nRows = row[1]
    print(colValue + ', ' + str(nRows))
    selRows = (int)(nRows * PERCENTAGE);
    #SQL-Server specific syntax for random selection
    innerQuery = "SELECT TOP " + str(selRows) + " *" +" FROM " + tableStrat + " WHERE " + columnStrat + "='"+colValue+"'" + " ORDER BY newid()"
    cursorInn = cnxnInn.cursor()
    rows = cursorInn.execute(innerQuery)
    if first:
        writer.writerow([x[0] for x in cursorInn.description])  # column headers
        first = False
    for row in rows:
        writer.writerow(row)
    cursorInn.close()
cursor.close()
cnxn.close()
cnxnInn.close()
csvfile.close()
