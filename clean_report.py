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

PATH = "/input/original_reports"
FILETRAIN = "RetailSales2018-2021.xlsx"
#FILECUSTOMER = "/customer_info_qb.xlsx"


def readCSVFile(filename):
    
    file = PATH + filename
    return (pd.read_csv(file, chunksize=1000000))
#%%

def readXLSFile(filename):
    
    file = PATH + filename
    file = filename
    return (pd.read_excel(file))

def clean(data):
    #drop first, second, and last row
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
    data['Lease ID'] = data['Lease Name']
    data['Lease ID'] = data['Lease ID'].map(lambda x: 
                                            x[x.find('(')+1:x.find(')')-1])
    
    
    
#%%
    
    return data
()
if __name__ == '__main__':
    
    df_train = readXLSFile(FILETRAIN)
    df_train = clean(df_train)