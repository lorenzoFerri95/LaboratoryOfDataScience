
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


#  http://calendario.eugeniosongia.com/formula.htm

def getDayOfWeek(date_Ymd):
    day_name= list(calendar.day_name)
    day = datetime.datetime.strptime(date_Ymd, '%Y%m%d').weekday()
    return day_name[day]




if __name__ == "__main__":

    time_file = open("time.csv")
    time_dict = DictReader(time_file)


    driver = '{ODBC Driver 17 for SQL Server}'
    server = 'tcp:apa.di.unipi.it'
    database = 'Group5HWMart' 
    username = 'group5' 
    password = 'w9hez' 
    connectionString = 'DRIVER={};SERVER={};DATABASE={};UID={};PWD={}'.format(
        driver, server, database, username, password
    )

    cnxn = pyodbc.connect(connectionString)
    cursor = cnxn.cursor()

    sql='INSERT INTO PROVA_Time(time_code, year, quarter, month, week, day, day_of_week) VALUES(?,?,?,?,?,?,?)'

    for row in time_dict:
        cursor.execute(sql,
        (row['time_code'], row['year'], getQuarter(int(row['month'])),
        row['month'], row['week'], row['day'], getDayOfWeek(row['time_code']) ) )
    
    cnxn.commit()

    time_file.close()
    cursor.close()
    cnxn.close()