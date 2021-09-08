#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 17:06:30 2021

@author: b7nguyen
"""

MONTH_LIST = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
              'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12' }


def format_sales_colname(data):
    #For each column name, check to see if first 3 letters is in the Month List
    #using mapping and change format to year/month format with string slicing.
    data.columns = data.columns.map(lambda x: '{year}/{month}'.format(month=MONTH_LIST[x[0:3]], 
                     year=x[4:]) if x[0:3] in MONTH_LIST else x)
    
    return data


def get_unique_year(data):
    #Set the dates to numerical values, set the index as the lease name. Need 
    #Category column
    ret_list = []
    data = data.iloc[:,data.columns.str.contains('Lease Name|Category|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec')]
    data = format_sales_colname(data)
    data.set_index('Lease Name', inplace=True)
    
    #Sum up sales by each unique category
    filtered_df = data.groupby(['Category']).sum()
    
    #Extrat the unique years
    years_list = filtered_df.columns.map(lambda x: x[0:x.find('/')]).unique()
    
    for years in years_list:
        ret_list.append({'label':str(years), 'value':str(years)})
    
    return(ret_list)  