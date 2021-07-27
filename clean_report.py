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

    else:
        ret_frame = pd.read_excel(file)
    
    return ret_frame

def readXLSFileSheets(**kwargs):
    ret_list= []
    all_sheets = False
     
    if 'filename' in kwargs:
        file = PATH + kwargs['filename']
    else:
        print("File name not provided")
        return False
    
    if 'all_sheets' in kwargs:
        if kwargs['all_sheets'] == True:
            xls = pd.ExcelFile(file)
            if len(xls.sheet_names) > 1:
                for i in xls.sheet_names:
                    ret_list.append(pd.read_excel(xls,i))
        return ret_list
                    
                    
        #ret_frame = pd.read_excel(xls, sheet_name=kwargs['sheet'])

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
    
    #remove total column
    data.drop(['Total'], axis=1, inplace=True)
    
    #create column for lease ID
#    data['Lease ID'] = data['Lease Name']
#    data['Lease ID'] = data['Lease ID'].map(lambda x: 
#                                            x[x.find('(')+1:x.find(')')-1])
    data.set_index('Lease Name', inplace=True)
  
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

    data.set_index('Tenant Name', inplace=True)
    
    return data


def joinCol(data1, data2):
    if(data1.empty):
        print('first dframe returned')
        return data2

    
    data = pd.concat([data1, data2], join='inner', axis=1)

    return data

if __name__ == '__main__':
    
    #Read every tab of from data file
    df_sales = readXLSFileSheets(filename=FILETRAIN, all_sheets=True)
    temp_df = pd.DataFrame()
    
    #If there is more than one tab, then the file is a list of dframes, else
    #clean the one tab
    if type(df_sales) == list:
        for i in df_sales:
            if temp_df.empty:
                temp_df = clean_sales_report(i)
            else:
                temp_df = pd.concat([temp_df, clean_sales_report(i)], join='outer', axis=1)
                
    #Drop any duplicated comlumns. We may fix this later    
    temp_df = temp_df.drop(labels=temp_df.columns[temp_df.columns.duplicated()], axis=1)
    
                    
    df_cat = readXLSFile(filename=FILE_ANALYSIS, sheet='Sales Category ')
    
    
    #df_sales = clean_sales_report(df_sales)
    df_cat = clean_category_report(df_cat)
    
    #Join from df_cat "Property Name" and "Category"
    df_sales = pd.concat([temp_df, df_cat], join='outer', axis=1)