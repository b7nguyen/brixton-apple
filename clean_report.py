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

if __name__ == '__main__':
    
    df_train = readXLSFile(FILETRAIN)