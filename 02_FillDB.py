# Fill DB

import pyodbc
from sys import argv
from csv import reader

# Connection to SQL Server
server = 'tcp:apa.di.unipi.it'
database = 'Group5HWMart'
username = 'group5'
password = 'w9hez'

connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};\
                    SERVER='+server+';DATABASE='+database+';\
                    UID='+username+';PWD='+password

cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()

# Open file
filename = argv[1] 
fp = open(filename + ".csv")
file = reader(fp)

header = next(file)

# Build query
tablename = "[Group5HWMart].[group5].[PROVA_"+ filename +"]"

placeholder = ["?" for i in range(len(header))]
placeholder = str(tuple(placeholder)).replace("'", "")

query = "INSERT INTO "+ tablename + " VALUES " + placeholder
for line in file:
    cursor.execute(query, tuple(line))
    
# Delete
#query = "DELETE FROM" + tablename
#cursor.execute(query)

cursor.commit()
cursor.close()
cnxn.close()
fp.close()