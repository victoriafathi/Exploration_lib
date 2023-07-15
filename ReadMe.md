# Exploration Module

A module for navigating and cleaning dirty tables.

## Description

This module provides general functions to handle and clean messy or dirty tables. It includes functions for normalizing column names, removing special characters, converting data types, handling missing values, and identifying unique values.

## Introduction

Acquiring and working with data in the health field can present unique challenges. Health data is often collected from various sources and may suffer from issues such as inconsistent formatting, missing values, and irregularities in naming conventions. These challenges can make it difficult to perform accurate analysis and draw meaningful insights from the data.

The purpose of this module is to provide a set of tools that facilitate the navigation and cleaning of dirty tables commonly encountered in the health field. By utilizing the functions provided by this module, you can streamline the data cleaning process and ensure the accuracy and integrity of your analyses.

## Features

- `clean_column_name`: Cleans and normalizes column names by converting to lowercase, removing special characters, and stripping leading/trailing spaces.
- `clean_str_column`: Cleans string columns by converting to lowercase, removing special characters, and stripping leading/trailing spaces.
- `get_plot_na`: Generates bar plots to visualize missing value counts in the table.
- `get_unique_value_col`: Computes unique values for each column in the table.
- `find_features`: Searches for column names and values that match a given regex pattern.

## Installation

You can install the module using pip:

```pip install module-name```

## Usage

```python
import module_name

# Example usage of functions
# ...

# Requirements
- Python 3.x
- pandas
- plotly

#Contributing
Contributions are welcome! If you find any issues or want to add new features, please submit a pull request.
