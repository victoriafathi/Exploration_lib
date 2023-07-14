#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import pandas as pd
import plotly as px
import unittest

####################################################################################################
# Cleaning 
####################################################################################################

def clean_column_name(table):
    table.columns = table.columns.str.lower()
    table.columns = [re.sub('(,)|(:)|(-)', '', x) for x in table.columns]
    table.columns = [re.sub('(_)', ' ', x) for x in table.columns]
    table.columns = [x.strip(' ') for x in table.columns]


def clean_str_column(table):
    for col in table.columns:
        if table[col].dtype == object:
            table[col] = table[col].str.lower()
            table[col] = table[col].str.replace('(,)|(:)|(-)', '', regex=True)
            table[col] = table[col].str.replace('(_)', ' ', regex=True)
            table[col] = table[col].str.strip(' ')


####################################################################################################
# Plotting        
####################################################################################################

def get_plot_na(table, axis):
    na_count = table.isna().sum(axis=axis).sort_values(ascending=False)
    if axis==0:
        labels={'index': 'features', 'value':'missing value count'}
        fig = px.bar(na_count, height=600, width=2000, labels=labels)

    else:
        labels={'index': 'number of missing value', 'value':'number of patients'}
        fig = px.bar(na_count.value_counts().sort_index(), height=600, width=2000, labels=labels)

    fig.update_layout(font_size=8, bargap=0.3)
    return fig


####################################################################################################
# Get or search 
####################################################################################################

def get_unique_value_col(table, string=False):
    '''
    table: pandas dataframe
    string: computes unique value only for columns containing string
    ''' 
    unique_value = []
    unique_value_str = set()
    for col in table.columns:
        unique_value.append(list(pd.unique(table[col])))
        if string and col != 'patient id':
            unique_value_str.update(set(pd.unique(table[col])))
    
    if string: 
        #even when the column dtype is str, some values are not string
        unique_value_str_clean = unique_value_str.copy()
        for el in unique_value_str:
            if not(isinstance(el, str)):
                unique_value_str_clean.remove(el)
        return(unique_value_str_clean)
    
    return pd.DataFrame({"unique_value": unique_value}, index=table.columns) 


def find_features(table, regex):
    r = re.compile(regex)
    
    #Search in name columns
    results_columns = (set(table.loc[:, table.columns.str.contains(r)].columns))
    
    #Search in values 
    str_columns = table.dtypes[df.dtypes == object].index #str columns
    results_value = table[str_columns].applymap(func=(lambda x: (r.search(x)) if pd.notnull(x) else x)).any()
    
    #combine results
    results_columns.update(results_value[results_value].index)
    
    return results_columns


if __name__ == '__main__':
    unittest.main()