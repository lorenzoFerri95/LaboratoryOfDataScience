# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 23:00:39 2018

@author: Anna
"""

from datetime import timedelta
import pyodbc

#connect to data source, using userName and userPWD
server = 'tcp:apa.di.unipi.it' 
database = 'pubs' 
username = 'lbi' 
password = 'pisa' 
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()

query="SELECT ord_date, count(*) AS counts FROM sales GROUP BY ord_date ORDER BY ord_date"
cursor.execute(query)
first = True
firstDate=''
for row in cursor:
    if first:
        firstDate = row[0]
        count = row[1]
        print("First order on: " + str(firstDate)  + " was " + str(count) + " pieces ")
        first = False
    else:
        lastDate = row[0]
        count = row[1]
        diff = lastDate - firstDate
        print("then after " + str(diff.days) +' days '+ str(count) + " pieces \n")
        firstDate = lastDate
cursor.close()
cnxn.close()

