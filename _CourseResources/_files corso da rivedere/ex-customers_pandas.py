#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:08:40 2020

@author: roberto
"""

import pandas as pd

# First solution is to use pandas.
# For the read csv, separator needs to be specified
data_sales = pd.read_csv("sales_by_customer_month_store.csv", sep=';')
data_customer = pd.read_csv("customer_info.csv", sep=';')
# Cutting users not from USA
data_customer = data_customer.loc[data_customer["country"] == "USA"]
# Joining table has to be done with the merge function
data_join = pd.merge(data_customer,data_sales, on="customer_id")
# We want to know how much females and males spent during a year on average each month
# So we either group two times, first we sum and then we do the average
data_result_1 = data_join.groupby(["store_id","gender","month_of_year"]).agg({"total_sales":"sum"})
data_result_1 = data_result_1.groupby(["store_id","gender"]).agg({"total_sales":"mean"})
data_result_1 = data_result_1.rename(index=str, columns={"total_sales": "yearly_average"})
print(data_result_1.to_string())
print("\n")
# Or we can group only once and then simply divide by the count of distinct months
data_result_2 = data_join.groupby(["store_id","gender"]).agg({"total_sales":"sum", "month_of_year":"nunique"})
data_result_2["yearly_average"] = data_result_2["total_sales"]/data_result_2["month_of_year"]
print(data_result_2[["yearly_average"]].to_string())
print("\n")