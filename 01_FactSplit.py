# Split fact.csv in three fact tables: gpu_sales, cpu_sales, ram_sales

from csv import DictReader, writer

# open fact.csv and create output files
fact_file = open("fact.csv")
gpu_file = open("gpu_sales2.csv", "w", newline = '')
cpu_file = open("cpu_sales2.csv", "w", newline = '')
ram_file = open("ram_sales2.csv", "w", newline = '')

# iterators for each file
fact = DictReader(fact_file)
gpu = writer(gpu_file)
cpu = writer(cpu_file)
ram = writer(ram_file)


# header
fields = ["time_code", "geo_code", "vendor_code", "sales_uds", "sales_currency"]
gpu.writerow(["gpu_code"] + fields)
cpu.writerow(["cpu_code"] + fields)
ram.writerow(["ram_code"] + fields)

# scan fact.csv and insert each row in the right output file
for line in fact:
    row = []
    for col in fields:
    	row.append(line[col])
    
    if line["gpu_code"] != '':
        row = [line["gpu_code"]] + row
        gpu.writerow(row)
    elif line["cpu_code"] != '':
        row = [line["cpu_code"]] + row
        cpu.writerow(row)
    elif line["ram_code"] != '':
        row = [line["ram_code"]] + row
        ram.writerow(row)
    else:
        print("Sales error")
    
fact_file.close()
gpu_file.close()
cpu_file.close()
ram_file.close()



