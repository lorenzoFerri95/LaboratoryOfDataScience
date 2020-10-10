# -*- coding: utf-8 -*-
"""
@author: Anna
"""

import sys, getopt
import xml.etree.ElementTree as ET  # libreria per trattare il file XML
import csv

def getAttributes(root):
    attNames = set()    # Set che conterrà i nomi degli attributi

    for row in root:
        # si itera per ogni Tag  row  presente all'interno del Tag  root
        # row.attrib ritorna la Dictionary con le coppie   nome attributo (key): valore attributo (value)
        for att in row.attrib.keys():   # si itera per ogni attributo della riga corrente
            attNames.add(att)    # si aggiunge il nome dell'attributo al Set
    return attNames

    # cioè l'insieme dei nomi degli attributi viene riempito iterando su ciascun nome di attributo presente nel file XML
    # e aggiungendo quei nomi al Set in modo da ottenere soltanto i nomi distinti.
    # si fa questo invece che aggiungere al Set solo i nomi della prima riga del file XML
    # perché se una row del file XML ha un Missing Value esso non viene riempito con un carattere speciale,
    # come avviene in altri formati di file, ma quell'attributo mancherà in quella row.
    # quindi per ottenere tutti i possibili attributi dobbiamo fare uno scan di tutte le row del file XML.


# questo codice sotto serve esattamente alla stessa cosa che abbiamo già visto nel file csv2arff:
# cioè ottenere i valori dei parametri da riga di comando

# Store input and output file names
ifile=''
ofile=''
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"i:o:")
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-i':
        ifile=a
    elif o == '-o':
        ofile=a
    else:
        print("Usage: %s -i input -o output /n" % sys.argv[0])




# la funzione  parse  legge il file e ne stora il contenuto in una Dictionary
# (grazie a questo possiamo scrivere la funzione  getAttributes  come visto sopra)
d = ET.parse(ifile)
root = d.getroot()   # ottengo la root, che in pratica è l'intera dictionary con i dati del file XML (useremo quindi root per tutto)
nrows = len(root)   # il numero di righe è la lenght della root
first = True
if nrows == 0:
    print("This file does not contain any row")   # se il file non ha righe
else:
    attNames = getAttributes(root)  # Set dei nomi degli attributi, ottenuto con la funzione definita prima

    fileOut = open(ofile,"w")   # si crea il file csv in output

    # si riempie la prima riga del file csv con i nomi degli attributi, divisi dal simbolo  ","
    # si deve cominciare a scrivere la virgola solo dopo il primo nome di attributo, e dopo l'ultimo nome non deve esserci.
    # un trucco per avere questo risultato è implementato quì:
    # si inizializza una variabile fittizia  first = True  che all'inizio, essendo True, fa si che la condizione quì sotto
    # skippi la prima virgola da scrivere e scriva direttamente il nome.
    # first poi diventa False e quindi all'iterazione successiva la virgola viene sempre scritta prima del nome dell'attributo.
    # (quindi dopo l'ultimo attributo ovviamente la virgola non ci sarà).
    for attn in attNames:
        if first:
            first = False
        else:
            fileOut.write(",")  # si scrive la virgola
        fileOut.write(attn)   # si scrive il nome dell'attributo
        
fileOut.write("\n");   # si va alla riga successiva del csv


for row in root:   # si itera per tutte le righe della dictionary che contiene i dati del file XML
    first = True   # la variabile first serve sempre per quel problema con la virgola che abbiamo visto sopra
    
    for attn in attNames:   # si itera per ogni attirbuto possibile
        if first:
            first = False
        else:
            fileOut.write(",")

        att = row.get(attn)   # si ottiene il valore dell'attributo corrente per la riga corrente del file XML
        if att is None: 
            fileOut.write("?")   # se quell'attributo per la riga corrente non è presente si scrive il simbolo  "?"  nel file csv
        else:
            fileOut.write(att)   # se non è nullo si scrive quel valore nel file csv

     # ogni volta che terminano gli attributi di una riga del file XML andiamo a capo nel file csv e passiamo alla riga successiva del file XML
    fileOut.write("\n")

fileOut.close()