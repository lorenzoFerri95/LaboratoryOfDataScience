
from csv import DictReader
import pyodbc

import calendar
import datetime 


def getQuarter(month):
    if month <= 3:
        return 'Q1'
    if month <= 6:
        return 'Q2'
    if month <= 9:
        return 'Q3'
    return 'Q4'



def daysToMonth(month, year):
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


#  http://calendario.eugeniosongia.com/formula.htm
def getDayOfWeek(day, month, year):
    day = int(day)
    month = int(month)
    year = int(year)

    day_num = (year +
    (year-1)//4 - (year-1)//100 + (year-1)//400 +
    daysToMonth(month, year) + day ) % 7

    weekDays = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    return weekDays[day_num]



if __name__ == "__main__":

    time_file = open("time.csv")
    time_dict = DictReader(time_file)


    driver = '{ODBC Driver 17 for SQL Server}'
    server = 'tcp:apa.di.unipi.it'
    database = 'Group5HWMart' 
    username = 'group5' 
    password = 'w9hez' 
    connectionString = 'DRIVER={};SERVER={};DATABASE={};UID={};PWD={}'.format(
        driver, server, database, username, password )

    cnxn = pyodbc.connect(connectionString)
    cursor = cnxn.cursor()

    sql='INSERT INTO PROVA_Time(time_code, year, quarter, month, week, day, day_of_week) VALUES(?,?,?,?,?,?,?)'

    for row in time_dict:
        cursor.execute(sql,
        (row['time_code'], row['year'],
        getQuarter(int(row['month'])),
        row['month'], row['week'], row['day'],
        getDayOfWeek(row['day'], row['month'], row['year']) ) )
    
    cnxn.commit()

    time_file.close()
    cursor.close()
    cnxn.close()