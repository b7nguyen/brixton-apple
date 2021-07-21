#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 15:51:56 2021

@author: b7nguyen
"""
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
from pandas2arff import pandas2arff
#from sklearn.tree.export import export_text

#from decorators import ml_init

import seaborn as sns
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

import pandas as pd
from pandas.api.types import is_numeric_dtype

from imblearn.over_sampling import SMOTENC

#import arff

import numpy as np
import math

PATH = "./input/orginial_reports"
FILETRAIN = "/RetailSales2018-2021.xlsx"
FILE_ANALYSIS = "/BC Mngd Retail Sales Analysis Q1 2021-2020_2021.05.03.xlsx"


def readCSVFile(filename):
    
    file = PATH + filename
    return (pd.read_csv(file, chunksize=1000000))
#%%

def readXLSFile(**kwargs):
    
    if 'filename' in kwargs:
        file = PATH + kwargs['filename']
    else:
        print("File name not provided")
        return False
    
    if 'sheet' in kwargs:
        xls = pd.ExcelFile(file)
        ret_frame = pd.read_excel(xls, sheet_name=kwargs['sheet'])
        #ret_frame = df[kwargs['sheets']]
        
        #ret_frame = ret_frame[kwargs['sheets']]
    else:
        ret_frame = pd.read_excel(file)
    
    return ret_frame

def clean_sales_report(data):
    #drop 0, 2, and last row
    data.drop([0,2,len(data)-1], inplace=True)
    data.reset_index(drop=True, inplace=True)
    
    #rename the columns with the first row and drop the row
    data.columns = data.iloc[0]
    data.drop([0], inplace=True)
    data.reset_index(drop=True, inplace=True)
    
    #remove the white space from front and end of string
    #TODO   
    for i in data.columns:
        data = data.rename(columns={i:i.lstrip().rstrip()})
        
    #remove the rows with nan for lease names
    data = data[data['Lease Name'].isna()==False]
    data.reset_index(drop=True, inplace=True)
        
    #create another column attribute for the complex name
    data['complex']=np.nan #initialize column
    index = 0 #tracks the next iteration or group of complexes
    for i in data[data.iloc[:,0].values == 'Total'].index:
        data.loc[index:i,'complex'] = data['Lease Name'][index]
        data.drop([index], inplace=True)
        index=i+1
    data.reset_index(drop=True, inplace=True)

        
    #remove the row that calculates total
    data = data[data['Lease Name']!='Total']
    data.reset_index(drop=True, inplace=True)
    
    #create column for lease ID
#    data['Lease ID'] = data['Lease Name']
#    data['Lease ID'] = data['Lease ID'].map(lambda x: 
#                                            x[x.find('(')+1:x.find(')')-1])
    
  
    return data


def clean_category_report(data):
    #drop row index 0,1,2
    data.drop([0,1,2], inplace=True)
    data.reset_index(drop=True, inplace=True)
    
    #rename the columns with the first row and drop the row
    data.columns = data.iloc[0]
    data.drop([0], inplace=True)
    data.reset_index(drop=True, inplace=True)
    
    #remove the white space from front and end of string
    #TODO 
    for i in data.columns:
        data = data.rename(columns={i:i.lstrip().rstrip()}) 
        
        
    data = data[data['Tenant Name'].isna()==False]
    #data.drop([*data[data['Tenant Name'].isna()].index.values], inplace=True)
  
    #create column for lease ID
#    data['Lease ID'] = data['Tenant Name']
#    data['Lease ID'] = data['Lease ID'].map(lambda x: 
#                                            x[x.find('(')+1:x.find(')')-1])

    return data


def joinCol(data1, data2):
    data1 = data1.set_index('Lease Name')
    data2 = data2.set_index('Tenant Name')
    
    data = pd.concat([data1, data2], join='inner', axis=1)

    return data

if __name__ == '__main__':
    
    df_sales = readXLSFile(filename=FILETRAIN)
    df_cat = readXLSFile(filename=FILE_ANALYSIS, sheet='Sales Category ')
    
    df_sales = clean_sales_report(df_sales)
    df_cat = clean_category_report(df_cat)
    
    #df_sales = joinCol(df_sales, df_cat)