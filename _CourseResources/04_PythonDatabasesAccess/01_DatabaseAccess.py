
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# esempio di come connettersi ad un DB e usare un cursore per ottenere i risultati di una query

import pyodbc

server = 'tcp:apa.di.unipi.it' 
database = 'Foodmart'   # accediamo solo al DB "foodmart"
username = 'lds' 
password = 'pisa' 
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)

cursor = cnxn.cursor()
#CURSOR AS ITERATOR
rows = cursor.execute("SELECT TOP 10 education, gender FROM customer")
print('gender education')

# si itera per tutte le righe del risultato e si printano i valori dei due attributi  gender ed  education
# accedendovi direttamente con il nome dell'attributo.
for row in rows:
    print(row.gender, row.education) 
cursor.close()

print()
print()

#META-DATA from cursor
cursor = cnxn.cursor()
sql ="SELECT TOP 2 * FROM customer"
cursor.execute(sql) 

# in  cursor.description  abbiamo alcune info sul risultato della query, tra cui il nome ed il data type degli attributi
for attributes in cursor.description:
    print("Name: %s, Type: %s " % (attributes[0], attributes[1]))
print()


#Dates
rows = cursor.fetchall()   # in questo caso carichiamo nella memoria centrale locale il contenuto del cursore

for row in rows:
    print(row.date_accnt_opened)   # accediamo alla stringa che rappresenta la data
    print(row.date_accnt_opened.date())   # printiamo la stringa trasformata in formato data.
    print(row.date_accnt_opened.astimezone())  # con questo nel risultato hai anche la time-zone
    
cursor.close()
print()
print()


# con questo si ottengono tutte le info sui META-DATA di tutte le tabelle nel DB
cursor = cnxn.cursor()
for table in cursor.tables():
    print(table)
    
print()
print()

# con questo solo le info delle tabelle di sistema (sys)
for table in cursor.tables(table='sys%'):
    print(table)   
    print(table.table_name)

print()
print()

# così si ottengono i nomi delle colonne della tabella  customers
for row in cursor.columns(table='customer'):
    print(row)

print()
print()
cursor.close()


#################################################

# altra connessione, questa volta per inserire i dati nel DB

import pyodbc 

server = 'tcp:apa.di.unipi.it' 
username = 'lbi' 
password = 'pisa'
database = 'lbi' 
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()



# scriviamo una query parametrica (con i "?" al posto dei valori),
# in modo da scrivere diverse righe nel DB con una sola query.


names = ['Anna', 'Valentina']
age = [30,20]

sql ="INSERT INTO test_insert(id,name,age) VALUES(?,?,?)"

for i in range(len(names)):
    rows = cursor.execute(sql, (i,names[i],age[i]))

cnxn.commit()  # le righe verranno scritte nel DB tutte insieme solo durante l'esecuzione del  commit


cursor.execute("SELECT * FROM test_insert;") 
rows = cursor.fetchall()
for row in rows:
    print(row)
cursor.close()
        