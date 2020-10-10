# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 09:58:40 2018

@author: Anna
"""




import pyodbc 

server = 'tcp:apa.di.unipi.it' 
database = 'lbi' 
username = 'lbi' 
password = 'pisa' 
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)

#META-DATA from cursor
cursor = cnxn.cursor()
sql ="SELECT TOP 2 * FROM census"
cursor.execute(sql) 

#Attribute name and type
for attributes in cursor.description:
    print("Name: %s, Type: %s " % (attributes[0], attributes[1]))
print()