# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 22:44:23 2018

@author: Anna
"""

# accesso al database e print del risultato della query

import pyodbc

#connect to data source, using userName and userPWD
server = 'tcp:apa.di.unipi.it' 
database = 'pubs' 
username = 'lds' 
password = 'pisa' 
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()

query="SELECT title, price FROM titles"
cursor.execute(query)
# scan results
for row in cursor:
    title = row.title
    price = row.price
    if price is not None:
        print (title + ", " +str(price))
        print(title + ", {0:.2f}".format(price))
    else:
        print(title)
cursor.close()
cnxn.close()