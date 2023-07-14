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
    """
    The function `clean_column_name` converts the column names of a table to lowercase, removes
    punctuation characters, replaces underscores with spaces, and removes leading and trailing spaces.
    
    :param table: The parameter "table" is expected to be a pandas DataFrame object
    """
    table.columns = table.columns.str.lower()
    table.columns = [re.sub('(,)|(:)|(-)', '', x) for x in table.columns]
    table.columns = [re.sub('(_)', ' ', x) for x in table.columns]
    table.columns = [x.strip(' ') for x in table.columns]


def clean_str_column(table):
    """
    The function `clean_str_column` takes a table as input and converts all string columns to lowercase,
    removes certain characters, replaces underscores with spaces, and removes leading and trailing
    spaces.
    
    :param table: The parameter "table" is expected to be a pandas DataFrame object
    """
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
    """
    The function `get_plot_na` takes a table and an axis as input, calculates the count of missing
    values along the specified axis, and returns a bar plot showing the count of missing values for each
    feature if axis=0, or the count of features with a specific number of missing values if axis=1.
    
    :param table: The table parameter is the DataFrame or table that you want to analyze for missing
    values. It should be in a format that can be processed by the pandas library
   
    :param axis: The "axis" parameter determines whether the missing value count is calculated for each
    feature (axis=0) or for each observation (axis=1)
    
    :return: a plotly bar chart object.
    """

    na_count = table.isna().sum(axis=axis).sort_values(ascending=False)
    if axis==0:
        labels={'index': 'features', 'value':'missing value count'}
        fig = px.bar(na_count, height=600, width=2000, labels=labels)

    else:
        labels={'index': 'number of missing value', 'value':'number of people'}
        fig = px.bar(na_count.value_counts().sort_index(), height=600, width=2000, labels=labels)

    fig.update_layout(font_size=8, bargap=0.3)
    return fig


####################################################################################################
# Get or search 
####################################################################################################

def get_unique_value_col(table, string=False):
    """
    The function `get_unique_value_col` returns a DataFrame or a list of unique values in each column of
    a given table, with an option to return only string values.
    
    :param table: The table parameter is the input table or dataframe that contains the data
    
    :param string: The "string" parameter is a boolean value that determines whether the function should
    return unique values as strings or not. If "string" is set to True, the function will return unique
    values as strings. If "string" is set to False, the function will return unique values as a
    DataFrame, defaults to False (optional)
    
    :return: The function `get_unique_value_col` returns a DataFrame containing the unique values for
    each column in the input table. If the `string` parameter is set to `True`, it also returns a list
    of unique string values across all columns, excluding the 'patient id' column.
    """

    unique_value = []
    unique_value_str = set()
    for col in table.columns:
        unique_value.append(list(pd.unique(table[col])))
    
    if string: 
        #even when the column dtype is str, some values are not string
        unique_value_str_clean = unique_value_str.copy()
        for el in unique_value_str:
            if not(isinstance(el, str)):
                unique_value_str_clean.remove(el)
        return(unique_value_str_clean)
    
    return pd.DataFrame({"unique_value": unique_value}, index=table.columns) 


def find_features(table, regex):
    """
    The function `find_features` takes a table and a regular expression as input, and returns a set of
    column names that match the regular expression in either the column names or the values of the
    table.
    
    :param table: The "table" parameter is a pandas DataFrame that represents a table of data. It could
    be any table with columns and rows
    
    :param regex: The regex parameter is a regular expression pattern that you want to search for in the
    table. It can be any valid regular expression pattern that you want to match against the column
    names and values in the table
    
    :return: The function `find_features` returns a set of column names from the input `table` that
    match the regular expression `regex`.
    """
    r = re.compile(regex)
    
    #Search in name columns
    results_columns = (set(table.loc[:, table.columns.str.contains(r)].columns))
    
    #Search in values 
    str_columns = table.dtypes[table.dtypes == object].index #str columns
    results_value = table[str_columns].applymap(func=(lambda x: (r.search(x)) if pd.notnull(x) else x)).any()
    
    #combine results
    results_columns.update(results_value[results_value].index)
    
    return results_columns


if __name__ == '__main__':
    unittest.main()