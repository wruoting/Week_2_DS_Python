# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:37:48 2019

@author: epinsky
@Modified: rwang
"""

# run this  !pip install pandas_datareader
from pandas_datareader import data as web
import os
import math
import numpy as np 
import pandas as pd

# This file has been updated with the weekly and daily volatility calculations

ticker='WMT'
ticker_file = './{}.csv'.format(ticker)
output_file = '{}_weekly_return_volatility.csv'.format(ticker)

try:
    df = pd.read_csv(ticker_file)
    start_date = '2014-01-01'; 
    end_date = '2018-12-31'
    df = df[df['Date'] >= start_date]
    df = df[df['Date'] <= end_date]
    df['Return'] = df['Adj Close'].pct_change()
    df['Return'].fillna(0, inplace = True)
    df['Return'] = 100.0 * df['Return']
    df['Return'] = df['Return'].round(3)        
    df_2 = df[['Year', 'Week_Number', 'Return']]
    df_2.index = range(len(df))
    df_grouped = df_2.groupby(['Year', 'Week_Number'])['Return'].agg([np.mean, np.std])
    df_grouped.reset_index(['Year', 'Week_Number'], inplace=True)
    df_grouped.rename(columns={'mean': 'mean_return', 'std':'volatility'}, inplace=True)
    df_grouped.fillna(0, inplace=True)
    df_grouped.to_csv(output_file, index=False)
    
except Exception as e:
    print(e)
