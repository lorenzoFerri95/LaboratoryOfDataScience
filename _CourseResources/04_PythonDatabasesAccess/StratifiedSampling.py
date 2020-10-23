# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 18:01:46 2018

@author: Anna
"""

'''
il problema che dobbiamo risolvere quì è fare un sample di dati dove le percentuali di oggetti con valori
diversi dell'attributo 'sex' vengono presenrvate. (es. se all'inizio il dataset è composto da 60% Maschi e 40% Femmine
allora dopo il sample le percentuali di Maschi e Femmine devono essere le stesse).
'''

import pyodbc
import csv
import random



def randomCsv(cursor, file_w, tot, to_sel):
    #output result set choosing to_sel rows randomly from tot
    for row in cursor:
        #probability of selecting current row
        prob = to_sel / float(tot) 
        ran = random.random()
        #print ("to_sel %f tot %f prob %f rand %f " %(to_sel, tot, prob,ran))
        if ran < prob:
            file_w.writerow(row)  # si scrive la riga solo se il numero casuale è minore della probabilità desiderata
            to_sel= to_sel - 1
        tot = tot - 1
     

PERCENTAGE=0.30
tableStrat= 'census'
columnStrat='sex'
outputFile= 'selection-rcsv.csv' 
csvfile = open(outputFile, 'w', newline='')
writer = csv.writer(csvfile)
   
#connect to data source, using userName and userPWD
server = 'tcp:apa.di.unipi.it' 
database = 'lbi' 
username = 'lbi' 
password = 'pisa' 
connectionString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password
cnxn = pyodbc.connect(connectionString)
cursor = cnxn.cursor()

# questa query fa un raggruppamento per Sex (maschi e femmine) e conta gli oggetti in ogni gruppo

query = "SELECT " + columnStrat + ", COUNT(*)" + " FROM " + tableStrat + " GROUP BY " + columnStrat
cursor.execute(query)          

first = True
cnxnInn = pyodbc.connect(connectionString)

# il risultato della query ha solo due righe (una per ogni valore del sex)
# iteriamo per queste due righe e otteniamo i valori del conteggio per ogni gruppo

for row in cursor:
    colValue = row[0]
    nRows = row[1]
    print(colValue + ', ' + str(nRows))
    selRows = int((nRows * PERCENTAGE))   # numero di righe da selezionare casualmente (numero righe * 30%)
    #SQL-Server specific syntax for random selection
    innerQuery = "SELECT  *" +" FROM " + tableStrat + " WHERE " + columnStrat + "='"+colValue+"'"
    cursorInn = cnxnInn.cursor()
    rows = cursorInn.execute(innerQuery)
    if first:
        writer.writerow([x[0] for x in cursorInn.description])  # column headers
        first = False
    randomCsv(rows,writer, nRows, selRows)
    cursorInn.close()
    
cnxnInn.close()
cursor.close()
cnxn.close()
csvfile.close()
