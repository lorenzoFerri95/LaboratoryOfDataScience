

def getQuarter(month):
    if month <= 3:
        return 'Q1'
    if month <= 6:
        return 'Q2'
    if month <= 9:
        return 'Q3'
    return 'Q4'


'''
'Friday'  '20130322'
'Saturday'
'Sunday'
'Monday'
'Tuesday'
'Wednesday'
'Thursday'
'''



if __name__ == "__main__":

    from csv import DictReader

    time_file = open("time.csv")
    time_dict = DictReader(time_file)



    import pyodbc

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

    #sql='DELETE FROM PROVA_Time'
    #cursor.execute(sql)

    for row in time_dict:
        cursor.execute(sql,
        (row['time_code'], row['year'], getQuarter(int(row['month'])),
        row['month'], row['week'], row['day'], 0 ) )
        break

    cnxn.commit()

    time_file.close()
    cursor.close()
    cnxn.close()