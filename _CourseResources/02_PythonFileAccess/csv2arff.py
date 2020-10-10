# -*- coding: utf-8 -*-
"""
@author: Anna

- trasformare un file  CSV  in un file  ARFF

i file CSV possono avere o no l'Header con i Meta-Data.
quindi creiamo due categorie di funzioni diverse:
una che funziona quando il file CSV non ha l'Header (funzioni con nome senza  h  in fondo),
e l'altra che funziona quando ce l'ha  (funzioni con nome con  h  in fondo, es.  csv2arff_h).

commentiamo solo il caso con Header, è facile poi fare le stesse considerazione per il file senza Header.

"""


import sys
import getopt  # vediamo questa alla fine
import csv   # libreria che permette di lavorare con i file csv in python

def is_number(s):
    """ funzione per verificare se l'argomento è un numero o no """
    try:
        float(s)
        return True
    except ValueError:
        return False



def getType_h(ifile, MAX_ENUMERATED = 3):
    """ si ottiene il data type di ciascuna colonna in un file csv con header.
    MAX_ENUMERATED  è il numero di valori distinti sopra il quale il data type non è più categorico """

    fileIn = open(ifile)   # aprire il file csv in sola lettura

    attrs = fileIn.readline().strip().split(',')   # creare una lista con i nomi di tutti gli attributi della tabella nel CSV
    nattrs = len(attrs)  # numero di attributi

    # lista con un numero di  True  pari al numero di attributi, che riempiremo poi con True o False in base a che
    # l'attributo corrispondente sia un attributo numerico (True) o no (False).
    atype = [True] *  nattrs
    
    # inizializziamo una lista che riempiamo con un numero di  Set  pari al numero di attributi
    # in questi Set ci andranno i valori di ogni attributo, ed essendo un Set manterrà solo i valori distinti.
    # questo quindi ci servirà per determinare se il numero di valori distinti dell'attributo supera il valore di MAX_ENUMERATED
    distinctValues = []
    for k in range(nattrs):
        distinctValues.append(set())
    
    #get types analyzing the others lines
    lines = csv.reader(fileIn, delimiter = ',')
    for row in lines:   # itero su ogni riga
        for k in range(nattrs):   # itero su ogni colonna, quindi su ogni cella della riga corrente
            if row[k] == '?':     # se il valore in quella cella è nullo passo avanti
                pass
            else:
                # modifichiamo il valore della lista  atype  mantenendo True se l'attributo è numerico e False se non lo è.
                # per fare ciò si verifica se nella cella corrente c'è un valore che non è numerico, se è così
                # il valore nella lista riferito all'attributo corrispondente diventa False.
                atype[k] = atype[k] & is_number(row[k])
                if len(distinctValues[k]) <= MAX_ENUMERATED:
                    # aggiungiamo il valore della cella corrente al Set di valori distinti nella lista   distinctValues,
                    # solo finché il numero di valori distinti già presenti nel Set è uguale al parametro MAX_ENUMERATED,
                    # quindi fino a che nei Set saranno presenti esattamente un numero di numero di valori pari a
                    # MAX_ENUMERATED + 1,  perché quando il numero di valori distinti è pari a MAX_ENUMERATED
                    # la condizione è comunque verificata e quindi si aggiunge un ulteriore valore.
                    # questo perché una volta che il nuero di valori distinti diventa superioire anche solo di 1
                    # al parametro MAX_ENUMERATED sappiamo già che quell'attributo non è categorico perché ha superato
                    # il threshold fissato  (andare avanti inserendo altri valori distinti quindi diventa inutile e costoso).
                    distinctValues[k].add(row[k])
    fileIn.close  
    
    
    # infine riempiamo una lista con i data type di ogni colonna in ordine
    finalTypes = []

    for k in range(nattrs):
        # caso in cui i valori distinti dell'attributo sono maggiori del threshold fissato
        if len(distinctValues[k]) > MAX_ENUMERATED:
            if atype[k] == True:
                finalTypes.append('numeric')   # se in  atype  in corrispondenza di k abbiamo True l'attributo è numerico 
            else: 
                finalTypes.append('string')  # se in  atype  in corrispondenza di k abbiamo False l'attributo è una stringa
        
        # caso in cui i valori distinti dell'attributo sono minori del threshold fissato, il Data Type è  Enumerated
        # dobbiamo creare un Set con tutti i valori distinti che ciascun attributo può assumere,
        # perché il Data Type Enumerate deve essere seguito dai possibili valori categorici.
        else:
            res = "{"
            first = True
            for s in distinctValues[k]:
                if first:
                    first = False
                else:
                    res += ","
                res += s
            res += "}"  
            finalTypes.append(res)
    return attrs, finalTypes


# stessa cosa di questo sopra ma per file senza header
def getType(ifile,MAX_ENUMERATED = 3):
    
    fileIn = open(ifile)
    
    lines = csv.reader(fileIn, delimiter = ',')
    
    distinctValues = []
    atype = []
    nattrs = 0
    first_line = True
    
    for row in lines:
        if first_line:
            #Initialize data structures 
            nattrs = len(row)
            atype = [True] *  nattrs
            for k in range(nattrs):
                distinctValues.append(set())
            first_line = False
            
        for k in range(nattrs):
            if row[k] == '?':
                pass
            else:
                atype[k] = atype[k] & is_number(row[k])
                if len(distinctValues[k]) <= MAX_ENUMERATED:
                    distinctValues[k].add(row[k])
    fileIn.close   
    
    finalTypes = []
    for k in range(nattrs):
        if len(distinctValues[k]) > MAX_ENUMERATED:
            if atype[k] == True:
                finalTypes.append('numeric')
            else: 
                finalTypes.append('string')
        else:
            #enumerated - construct string
            res = "{"
            first = True
            for s in distinctValues[k]:
                if first:
                    first = False
                else:
                    res += ","
                res += s
            res += "}"  
            finalTypes.append(res)     
    return finalTypes



def csv2arff_h(ifile, ofile):

    fileOut = open(ofile,"w")    # si crea il nuovo file di output aprendo un file, che non esiste già, con diritto di scrittura.
    fileOut.write("@RELATION "+ofile+"\n")   # il nome della relazione è semplicemente il nome del file.
   
    # dal file di input otteniamo il nome ed il Data Type degli attributi mediante la funzione dichiarata sopra.
    attrs, attTypes = getType_h(ifile, MAX_ENUMERATED = 2)
    
    # i Meta-Data vengono scritti all'inizio del nuovo file arff:   @ATTRIBUTE nome_attributo data_type_attributo
    for k in range(len(attTypes)):   
        fileOut.write("@ATTRIBUTE "+ attrs[k]+" "+ attTypes[k] +"\n")
    
    
    fileOut.write("@DATA \n");   # quando i Meta-Data sono finiti scriviamo  @DATA per indicare che da li cominciano i dati

    # tutto il resto dei dati possono essere scritti nel file arff leggendo direttamente quelli del file csv
    # (in pratica è una copia).  si salta solo la prima riga del file CSV, perché contiene l'Header che abbiamo già processato,
    # con  fileIn.readline()
    fileIn = open(ifile);
    fileOut.writelines(fileIn.readlines())
    fileIn.close()
    fileOut.close()



def csv2arff(ifile, ofile):

    fileOut = open(ofile,"w") 
    fileOut.write("@RELATION "+ofile+"\n")  

    attTypes = getType(ifile, MAX_ENUMERATED = 2)

    for k in range(len(attTypes)):   
        fileOut.write("@ATTRIBUTE column-"+ str(k) +" "+ attTypes[k] +"\n")
    #write data
    fileOut.write("@DATA \n");
    fileIn = open(ifile);
    fileOut.writelines(fileIn.readlines())
    fileIn.close()
    fileOut.close()
 



    
'''----------------------- MAIN PROGRAM -----------------------------

nel programma principale ci va questo codice.
questo permette di inserire manualmente gli argomenti delle funzioni che ci servono nel nostro programma
quando runniamo il programma da riga di comando.

cioè se runniamo il programma dalla Prompt con il comando:    >> python programma.py
possiamo passare anche dei valori dopo questo comando.
questi saranno i valori dei parametri che ci servono dentro il programma per le nostre funzioni, in fila,
es. in questo caso:     >> python programma.py -i input_file.csv -o output_file.arff -h y/n

dopo  -i  abbiamo il nome del file in input
dopo  -o  abbiamo il nome del file in output
dopo  -h  abbiamo  y  se il file contiene Header o  n  se non lo contiene.

il metodo  getopt.getopt  permette di accedere ai valori inseriti come argomenti durante l'esecuzione del programma dalla Prompt
dobbiamo specificare che questi valori si trovano in    sys.argv[1:]
cioè si trovano nella lista di argomenti passati manualmente nella Prompt dopo il primo
(il primo è sempre il nome del programma).
inoltre dobbiamo specificare le  opzioni e la presenza eventuale di argomenti:
l'opzione è ciò che deve essere scritto nella Prompt (preceduto dal simbolo  - ) per indicare quale opzione stiamo trattando
es.  scrivendo  i  la Prompt saprà che stiamo trattando l'opzione  i
in più dobbiamo aggiungere il simbolo  :  dopo ogni opzione che richiede successivamente un argomento
(che comunque non è obbligatorio)

una volta ottenuti i valori degli argomenti inseriti dall'utente che ha runnato il programma tramite Prompt
possiamo storare il valore di questi argomenti in variabili che poi verranno usate nel programma.
es. il valore  y o n  dell'opzione  -o  viene testato per verificare se il file CSV ha l'Header o no,
in modo da usare l'apposita funzione per trasformarlo.
l'argomento dopo  -i  viene usato come argomento della funzione per la trasformazione riferito al nome del file da leggere.
ecc...
'''
    
# Store input and output file names
ifile=''
ofile=''
# Read command line args
myopts, args = getopt.getopt(sys.argv[1:],"i:o:h:")
###############################
# o == option
# a == argument passed to the o
###############################
for o, a in myopts:
    if o == '-i':
        ifile=a
    elif o == '-o':
        ofile=a
    elif o == '-h':
        head=a
    else:
        print("Usage: %s -i input -o output -h y/n" % sys.argv[0])

if head == 'y':
    csv2arff_h(ifile,ofile)
else:
    csv2arff(ifile,ofile)
