#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:28:57 2020

@author: roberto
"""

import csv
from pprint import pprint
#open files and use dictreader to cache information
file1 = open("sales_by_customer_month_store.csv", mode='r', encoding='utf-8-sig')
csv_sales = csv.DictReader(file1, delimiter = ";")
file2 = open("customer_info.csv", mode='r', encoding='utf-8-sig')
csv_customer = csv.DictReader(file2, delimiter = ";")
#select only customers born in USA
customers_usa_gender = dict()
for line in csv_customer:
    if line["country"] == "USA":
        c_id = int(line["customer_id"])
        customers_usa_gender[c_id] = line["gender"]
file2.close()
#groupby and aggregation
store_gender_info = dict()
for line in csv_sales:
    c_id = int(line["customer_id"])
    if c_id in customers_usa_gender:
        s_id = int(line["store_id"])
        if s_id not in store_gender_info:
            store_gender_info[s_id] = dict()
        gender_info = store_gender_info[s_id]
        gender = customers_usa_gender[c_id]
        if gender not in gender_info:
            gender_info[gender] = {"total_sales" : 0, "distinct_months" : set()}
        m_y = int(line["month_of_year"])
        gender_info[gender]["total_sales"] += float(line["total_sales"])
        gender_info[gender]["distinct_months"].add(m_y)
file1.close()
#caclulating yearly average
for store in store_gender_info:
    for gender in store_gender_info[store]:
        info = store_gender_info[store][gender]
        info["yearly_average"] = info["total_sales"]/len(info["distinct_months"])
        keys = ["yearly_average"]
        new_dict = { key: info[key] for key in keys }
        store_gender_info[store][gender] = new_dict
#printing result
pprint(store_gender_info)