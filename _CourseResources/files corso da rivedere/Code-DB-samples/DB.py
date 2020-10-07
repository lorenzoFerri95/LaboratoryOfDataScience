
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyodbc 

server = 'tcp:apa.di.unipi.it' 
database = 'Foodmart' 
username = 'lbi' 
password = 'pisa' 
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)

cursor = cnxn.cursor()
#CURSOR AS ITERATOR
rows = cursor.execute("SELECT TOP 10 education, gender FROM customer")
print('gender education') 
for row in rows:
    print(row.gender, row.education) 
cursor.close()

print()
print()

#META-DATA from cursor
cursor = cnxn.cursor()
sql ="SELECT TOP 2 * FROM customer"
cursor.execute(sql) 

#Attribute name and type
for attributes in cursor.description:
    print("Name: %s, Type: %s " % (attributes[0], attributes[1]))
print()


#Dates
rows = cursor.fetchall() 
for row in rows:
     print(row.date_accnt_opened)
     print(row.date_accnt_opened.date())
  #   print(row.date_accnt_opened.astimezone())
    
cursor.close()
print()
print()


#META-DATA on TABLES
cursor = cnxn.cursor()
for table in cursor.tables():
    print(table)   
    
print()
print()

for table in cursor.tables(table='sys%'):
    print(table)   
    print(table.table_name)

print()
print()

# columns in table x
for row in cursor.columns(table='customer'):
    print(row)

print()
print()
cursor.close()


import pyodbc 

server = 'tcp:apa.di.unipi.it' 
username = 'lbi' 
password = 'pisa'
database = 'lbi' 
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()



#Query with parameters
names = ['Anna', 'Valentina']
age = [30,20]

#dele = "delete from test_insert where id=0 or id=1"
#cursor.execute(dele)

sql ="INSERT INTO test_insert(id,name,age) VALUES(?,?,?)"

for i in range(len(names)):
    rows = cursor.execute(sql, (i,names[i],age[i]))

cnxn.commit()
cursor.execute("SELECT * FROM test_insert;") 

rows = cursor.fetchall() 

for row in rows:
     print(row)
cursor.close()
        