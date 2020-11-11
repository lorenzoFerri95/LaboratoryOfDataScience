# Load dimensions' tables to SQL Server

import pyodbc
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

# Dimensions' files (except time) and corresponding table names in SQL Server
files_tables = [("cpu.csv", "Cpu_Product"), ("geography.csv", "Geography"),\
                ("gpu.csv", "Gpu_Product"), ("ram.csv", "Ram_Product"),\
                ("vendor.csv", "Vendor")]

# Iterates for each dimensions' file
for filename, table in files_tables:
    # Open file
    fp = open(filename)
    file = reader(fp)
    header = next(file)
    
    # Build query
    tablename = "[Group5HWMart].[group5].["+ table +"]"
    placeholders = "?"
    for i in range(len(header) - 1): 
        placeholders += ",?"
    
    query = "INSERT INTO "+ tablename + " VALUES " + "("+placeholders+")"
    
    # Execute queries
    for line in file:
        cursor.execute(query, tuple(line))
    
    # close file
    fp.close()

# Commit and close connection
cursor.commit()
cursor.close()
cnxn.close()





