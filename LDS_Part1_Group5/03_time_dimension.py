
from csv import DictReader
import pyodbc


def getQuarter(month):
    """ottenere il quarter dato il mese """
    month = int(month)

    if month <= 3:
        return 'Q1'
    if month <= 6:
        return 'Q2'
    if month <= 9:
        return 'Q3'
    return 'Q4'


'''formula che abbiamo usato per ottenere il giorno della settimana dalla data:
http://calendario.eugeniosongia.com/formula.htm'''

def daysToMonth(month, year):
    """dato il mese ed anno si ottiene il numero di giorni trascorsi\
    dall'inizio dell'anno all'inizio del mese.
    questa funzione è usata nella funzione per ottenere il giorno della settimana"""

    if month == 1:
        return 0
    elif month in (5, 7, 10, 12):
        return 30 + daysToMonth(month-1, year)
    elif month in (2, 4, 6, 8, 9, 11):
        return 31 + daysToMonth(month-1, year)
    elif month == 3:
        if year%400 == 0 or (year%4 == 0 and year%100 != 0):
            return 29 + daysToMonth(month-1, year)
        else:
            return 28 + daysToMonth(month-1, year)
    else:
        print('error')


def getDayOfWeek(day, month, year):
    """data la data in formato numerico si ottiene il giorno della settimana con la formula"""

    day = int(day)
    month = int(month)
    year = int(year)

    day_num = (year + (year-1)//4 - (year-1)//100 + (year-1)//400 + daysToMonth(month, year) + day ) % 7

    weekDays = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    return weekDays[day_num]


def to_date(date):
    """ trasforma la data in formato yyyymmdd nel formato yyyy-mm-dd,\
    accettato da SQL Server come formato standard per la data"""
    return date[:4] + '-' + date[4:6] + '-' + date[6:]


if __name__ == "__main__":

    time_file = open("time.csv")
    time_dict = DictReader(time_file)

    driver = '{ODBC Driver 17 for SQL Server}'
    server = 'tcp:apa.di.unipi.it'
    database = 'Group5HWMart' 
    username = 'group5' 
    password = 'w9hez' 
    connectionString = 'DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4}'.format(
        driver, server, database, username, password )

    cnxn = pyodbc.connect(connectionString)
    cursor = cnxn.cursor()

    sql='''\
    USE [Group5HWMart]
    INSERT INTO [Time](time_code, year, quarter, month, week, day, day_of_week)\
    VALUES(?,?,?,?,?,?,?)'''

    for row in time_dict:
        cursor.execute(sql,
        (to_date(row['time_code']), row['year'], getQuarter(row['month']), row['month'],
        row['week'], row['day'], getDayOfWeek(row['day'], row['month'], row['year']) ) )
    
    cnxn.commit()

    time_file.close()
    cursor.close()
    cnxn.close()