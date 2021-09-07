#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 15:54:36 2021

@author: b7nguyen
"""
import pandas as pd
import numpy_financial as npf
import numpy as np

import plotly.offline as pyo
import plotly.graph_objs as go

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash

from datetime import date as dt
import requests
import dash_auth

MONTH_LIST = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
              'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12' }

dframe = pd.read_excel('cleaned_report.xlsx')
app = dash.Dash()

dframe = dframe.sort_values('Lease Name')

lease_names = []
for names in dframe['Lease Name'].unique():
    lease_names.append({'label':str(names),'value':str(names)})
    

app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(id='lease_picker',options=lease_names)
])

    

@app.callback(output=Output('graph', 'figure'),
              inputs=[Input('lease_picker', 'value')])
def make_report_lease_sales(lease):
    
    #Set the dates to numerical values, set the index as the lease name, and sort 
    #the dates in order
    data = dframe[dframe['Lease Name'] ==lease]
    data = data.iloc[:,dframe.columns.str.contains('Lease Name|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec')]
    data = format_sales_colname(data)
    data.set_index('Lease Name', inplace=True)
    data = data[sorted(data.columns)]
    
    traces = []

    #For each row or index name, extract only columns with sales > 100
    #Then create a line or Scatter object for that 
    for name in data.index:
        temp = data.loc[[name]]  #Work with one row at a time, double bracket returns dframe
        col = temp.values > 100  #col is an array of booleans
        temp = temp.iloc[:,col[0]] #Since there is only one item in dataframe, we can access it at [0]
        
        #Make a list of the traces
        traces.append(go.Scatter(
                x=temp.columns,
                y=temp.loc[name],
                mode='markers+lines',
                name=name))
    
#
    layout = go.Layout(
        title='Period to Period Comparison',
        hovermode='closest'
    )
    
    return { #In this case, the output is to a figure. Figures expect data and layout as parameters
        'data': traces,
        'layout': layout
    }

    
#%%

def format_sales_colname(data):
    #For each column name, check to see if first 3 letters is in the Month List
    #using mapping and change format to year/month format with string slicing.
    data.columns = data.columns.map(lambda x: '{year}/{month}'.format(month=MONTH_LIST[x[0:3]], 
                     year=x[4:]) if x[0:3] in MONTH_LIST else x)
    
    return data

if __name__ == '__main__':
    #pass
    app.run_server()