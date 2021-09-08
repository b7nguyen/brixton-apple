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
import report_methods as rtm



dframe = pd.read_excel('cleaned_report.xlsx')
app = dash.Dash()

dframe = dframe.sort_values('Lease Name')


lease_names = []
unique_years = []

for names in dframe['Lease Name'].unique():
    lease_names.append({'label':str(names),'value':str(names)})
    

unique_years = rtm.get_unique_year(dframe)


app.layout = html.Div([
    dcc.Graph(id='sales_by_lease_graph'),
    dcc.Dropdown(id='lease_picker',options=lease_names, value=lease_names[0]['value']),
    dcc.Graph(id='sales_by_category'),
    dcc.Dropdown(id='year_picker',options=unique_years, value=unique_years[0]['value'])
])
    
    
 
@app.callback(output=Output('sales_by_category', 'figure'),
              inputs=[Input('year_picker', 'value')])
def make_report_category_sales(year):
    
    #Set the dates to numerical values, set the index as the lease name. Need 
    #Category column
    data = dframe.iloc[:,dframe.columns.str.contains('Lease Name|Category|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec')]
    data = rtm.format_sales_colname(data)
    data.set_index('Lease Name', inplace=True)
    
    #Sum up sales by each unique category
    filtered_df = data.groupby(['Category']).sum()
    
    
    temp_year = [x for x in filtered_df.columns if year in x]
    total = filtered_df[temp_year].sum(axis=1)
    filtered_df['Total ' + str(year)] = total
    
    trace = go.Pie(labels=total.index, values=total.values)
    data = [trace]
    layout = go.Layout(
            title='Sales per category by year',
            title_x=.5,
            hovermode='closest')
    
    fig = go.Figure(data=data, layout=layout)

    return(fig)
    
    
    
@app.callback(output=Output('sales_by_lease_graph', 'figure'),
              inputs=[Input('lease_picker', 'value')])
def make_report_lease_sales(lease):
    
    #Set the dates to numerical values, set the index as the lease name, and sort 
    #the dates in order
    data = dframe[dframe['Lease Name'] == lease]
    data = data.iloc[:,dframe.columns.str.contains('Lease Name|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec')]
    data = rtm.format_sales_colname(data)
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
        title_x=.5,
        hovermode='closest',
        
    )
    
    
    fig = go.Figure(data=traces, layout=layout)
    
    return(fig)
    
#    return { #In this case, the output is to a figure. Figures expect data and layout as parameters
#        'data': traces,
#        'layout': layout
#    }

    
#%%



if __name__ == '__main__':
    #pass
    app.run_server()