# Split fact.csv in three fact tables: Gpu_sales, Cpu_sales, Ram_sales.
# Load to SQL Server 

import pyodbc
from csv import DictReader

def to_date(date):
    return date[:4] + '-' + date[4:6] + '-' + date[6:]

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

# Open fact.csv 
fact_file = open("fact.csv")
fact = DictReader(fact_file)
# Header
fields = ["time_code", "geo_code", "vendor_code", "sales_uds", "sales_currency"]

# Build queries
gpu_sql = "INSERT INTO [Group5HWMart].[group5].[Gpu_sales](gpu_code, time_code, geo_code, vendor_code, sales_usd, sales_currency) VALUES (?,?,?,?,?,?)" 
cpu_sql = "INSERT INTO [Group5HWMart].[group5].[Cpu_sales](cpu_code, time_code, geo_code, vendor_code, sales_usd, sales_currency) VALUES (?,?,?,?,?,?)" 
ram_sql = "INSERT INTO [Group5HWMart].[group5].[Ram_sales](ram_code, time_code, geo_code, vendor_code, sales_usd, sales_currency) VALUES (?,?,?,?,?,?)" 

# Initialize lists of values to insert
gpu_values = []
cpu_values = []
ram_values = []

# Scan fact.csv and insert each record in the right list of values
for line in fact:
    # Change Date type
    line["time_code"] = to_date(line["time_code"])
    
    # Build record with all fields except [gpu|cpu|ram]_code
    record = [line[col] for col in fields]
    
    # Select output table and add [gpu|cpu|ram]_code
    if line["gpu_code"] != '':
        record = [line["gpu_code"]] + record
        gpu_values += [tuple(record)] 
    elif line["cpu_code"] != '':
        record = [line["cpu_code"]] + record
        cpu_values += [tuple(record)]
    elif line["ram_code"] != '':
        record = [line["ram_code"]] + record
        ram_values += [tuple(record)]
    else:
        print("Sales error")

# Close file
fact_file.close()

# Load fact tables
cursor.fast_executemany = True
cursor.executemany(gpu_sql, gpu_values)
cursor.executemany(cpu_sql, cpu_values)
cursor.executemany(ram_sql, ram_values)

# Commit and close connection
cursor.commit()
cursor.close()
cnxn.close()  

