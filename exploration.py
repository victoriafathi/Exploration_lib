#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import pandas as pd
import plotly as px
import matplotlib.pyplot as plt
#import seaborn as sns
import unittest

# Color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'

####################################################################################################
# Cleaning 
####################################################################################################

def clean_column_name(table):
    """
    The function `clean_column_name` converts the column names of a table to lowercase, removes
    punctuation characters, replaces underscores with spaces, and removes leading and trailing spaces.
    
    :param table: The parameter "table" is expected to be a pandas DataFrame object
    """
    table_copy = table.copy()
    table_copy.columns = table_copy.columns.str.lower()
    table_copy.columns = [re.sub('(,)|(:)|(-)', '', x) for x in table_copy.columns]
    table_copy.columns = [re.sub('(_)', ' ', x) for x in table_copy.columns]
    table_copy.columns = [x.strip(' ') for x in table_copy.columns]
    return table_copy

 
def clean_str_column(table):
    table_copy = table.copy()  # Create a copy of the DataFrame

    str_columns = table_copy.select_dtypes(include=['object']).columns
    table_copy[str_columns] = table_copy[str_columns].applymap(
        lambda x: re.sub('(,)|(:)|(-)', '', x.lower().strip()) if pd.notnull(x) and isinstance(x, str) else x) #remove , : and -, puts everything in lower caps and remove spaces at the beggining and end
    table_copy[str_columns] = table_copy[str_columns].applymap(
        lambda x: re.sub('_', ' ',  x) if pd.notnull(x) and isinstance(x, str) else x) #change underscore for space
    return table_copy

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
    for col in table.columns:
        unique_value.append(list(pd.unique(table[col])))
    
    unique_value_table = pd.DataFrame({"unique_value": unique_value}, index=table.columns) 

    if string: 
        unique_value_table.drop(unique_value_table.select_dtypes(exclude='object').columns, axis=1, inplace=True)

    return unique_value_table

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
    results_columns = set(table.columns[table.columns.str.contains(r)])
    
    #Search in values 
    str_columns = table.select_dtypes(include=['object']).columns
    results_value = table[str_columns].apply(lambda x: x.str.contains(r, na=False) if isinstance(str, x) else x).any()
    results_columns.update(results_value[results_value].index)
    
    #combine results
    results_columns.update(results_value[results_value].index)
    
    return results_columns

if __name__ == '__main__':
    data_test = pd.DataFrame({
    'Column1': ['Value1', 'Value2', 3, 4, 'Value_1', 3, 'Value3', 4],
    'Column:2': ['Value A', 'Val,ueB', 'ValueA', 'ValueC', 'ValueD', 'ValueB', 'ValueE', 'ValueE'],
    'Column_3': [True, False, True, False, False, True, True, True],
    'Column4-': [1.23, 4.56, 1.23, 7.89, 1.23, 7.89, 0.12, 4.56]
    })

    print(f"{GREEN}INITIAL TEST SET{RESET}")
    print(data_test)

    print(f"{GREEN} ############## TEST Cleaning functions ##############{RESET} ")
    
    print(f"{GREEN}\nTEST clean_column_name{RESET}")
    print(clean_column_name(data_test))
    expected_clean_column_name = pd.DataFrame({
    'column1': ['Value1', 'Value2', 3, 4, 'Value_1', 3, 'Value3', 4],
    'column2': ['Value A', 'Val,ueB', 'ValueA', 'ValueC', 'ValueD', 'ValueB', 'ValueE', 'ValueE'],
    'column 3': [True, False, True, False, False, True, True, True],
    'column4': [1.23, 4.56, 1.23, 7.89, 1.23, 7.89, 0.12, 4.56]
    })

    pd.testing.assert_frame_equal(clean_column_name(data_test), expected_clean_column_name)

    print(f"{GREEN}\nTEST clean_str_column{RESET}")
    print(clean_str_column(data_test))
    

    print(f"{GREEN} \n ############## TEST exploration functions ##############{RESET}")
    print(f"{GREEN}\nTEST get_unique_value_col{RESET}")

    print(get_unique_value_col(data_test, string=True))

    print(f"{GREEN}\nTEST find_features{RESET}")

    #find_features(data_test)