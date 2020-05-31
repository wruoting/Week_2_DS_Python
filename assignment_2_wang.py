# -*- coding: utf-8 -*-
"""
@author: rwang
"""
from pandas_datareader import data as web
import os
import math
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import scipy.stats as scipy

ticker='WMT'
ticker_file = os.path.join('./' + ticker + '.csv')


def number_of_days_positive_negative_returns(df, year):
    """
    df: pd dataframe. Data of interest
    year: int. The year of calculating positive and negative returns
    returns: Tuple with positive and negative days
    """
    year = str(year)
    # Return is calculated as a percentage, eg. 0.3 -> 0.3%
    start_date=year + '-01-01'; 
    end_date=year + '-12-31'
    df_returns = df.loc[((df['Date'] >= start_date) & (df['Date'] <= end_date))].copy()
    df_returns['Return'] = df['Return'] * 100
    returns_list = df_returns['Return']
    # Calculate number where returns are less than 0 in a series of returns
    returns_less_than_zero = returns_list.where(returns_list < 0).dropna().size
    # Calculate number where returns are greater than 0 in a series of returns
    returns_greater_than_zero = returns_list.where(returns_list > 0).dropna().size
    print('The number of days where returns are negative for the year {} are {}'.format(year, returns_less_than_zero))
    print('The number of days where returns are positive for the year {} are {}'.format(year, returns_greater_than_zero))
    return returns_greater_than_zero, returns_less_than_zero


def create_daily_returns(df, year):
    """
    df: pd dataframe. Data of interest
    year: int. The year of calculating positive and negative returns
    returns: a df with the following columns: year | trading days |  mu | % days < mu | % days > mu
    """
    # Calculate average daily return from a year of data, mu
    year = str(year)
    # Return is calculated as a percentage, eg. 0.3 -> 0.3%
    start_date=year + '-01-01'; 
    end_date=year + '-12-31'
    df_returns = df.loc[(df['Date'] >= start_date) & (df['Date'] <= end_date)].copy()
    df_returns['Return'] = df['Return'] * 100

    returns_list = df_returns['Return']
    total_days = returns_list.size
    mean = np.divide(returns_list.sum(), total_days)
    # Less than and greater than calculations
    less_than_mean = returns_list.where(returns_list < mean).dropna().size
    greater_than_mean = returns_list.where(returns_list > mean).dropna().size
    # Convert to percentages
    percent_less_than_mean = np.round(np.multiply(np.divide(less_than_mean, total_days), 100), 2)
    percent_greater_than_mean = np.round(np.multiply(np.divide(greater_than_mean, total_days), 100), 2)
    # Create series
    table = {'Year': year, 'Trading Days': [total_days], 'mu': [mean], '%% days < mu': [percent_less_than_mean], '%% days > mu': [percent_greater_than_mean]}
    return pd.DataFrame(data=table)

def create_daily_returns_with_std_deviation(df, year):
    """
    df: pd dataframe. Data of interest
    year: int. The year of calculating positive and negative returns
    returns: a df with the following columns: year | trading days |  mu | sigma | % days < mu - 2 * sigma | % days > mu - 2 * sigma
    """
    # Calculate average daily return from a year of data, mu
    year = str(year)
    # Return is calculated as a percentage, eg. 0.3 -> 0.3%
    start_date=year + '-01-01'; 
    end_date=year + '-12-31'
    df_returns = df.loc[(df['Date'] >= start_date) & (df['Date'] <= end_date)].copy()
    df_returns['Return'] = df['Return'] * 100

    returns_list = df_returns['Return']
    total_days = returns_list.size
    mean = np.divide(returns_list.sum(), total_days)
    std_deviation = returns_list.std()
    two_std_deviation = std_deviation * 2
    # Two std deviations fewer
    two_std_deviation_fewer = mean - two_std_deviation
    # Two std deviations greater
    two_std_deviation_greater = mean + two_std_deviation
    # Less than and greater than two standard deviations calculations
    less_than_two_std_deviations = returns_list.where(returns_list < two_std_deviation_fewer).dropna().size
    greater_than_two_std_deviations = returns_list.where(returns_list > two_std_deviation_greater).dropna().size
    # Convert to percentages
    percent_less_than_two_std_deviations = np.round(np.multiply(np.divide(less_than_two_std_deviations, total_days), 100), 2)
    percent_greater_than_two_std_deviations = np.round(np.multiply(np.divide(greater_than_two_std_deviations, total_days), 100), 2)
    # Create series
    table = {'Year': year, 'Trading Days': [total_days], 'mu': [mean], 'sigma': [std_deviation], '%% days < mu - 2 * sigma': [percent_less_than_two_std_deviations],
    '%% days > mu + 2 * sigma': [percent_greater_than_two_std_deviations]}
    return pd.DataFrame(data=table)


def main():
    df = pd.read_csv(ticker_file)
    years = range(2014, 2019)
    print('Question 1: ')
    for year in years:
        print('Year {}'.format(year))
        number_of_days_positive_negative_returns(df, year)
        print('------------------------------------------')

    print('Question 2: ')
    df_q2 = pd.DataFrame(columns=['Year', 'Trading Days', 'mu', '%% days < mu', '%% days > mu'])
    # Append each year to our dataframe
    for year in years:
        df_q2 = df_q2.append(create_daily_returns(df, year))
    print(df_q2)
    print('The average daily return between years varies from -0.12 % to 0.14 %. While the distribution of returns is generally assumed to be not normal, in 2016 the percentage of days with gains more than')
    print('mu and less than the mu were the same. Deviations from 50%% greater and less than mu were not larger than 2.78%. This does not indicate that the distribution is normal, but it would indicate ')
    print('that there is no incredibly high right or left skew. Interestingly, the years with below 0 daily average returns had a higher percentage of days trading greater than the mean. All other years have a greater percentage ')
    print('of days trading with returns below the mean. This implies that most years will have more negative trading days than positive trading days, which would follow a pattern of a mild right skew distribution.')

    print('Question 3 and Question 4: ')
    df_q3 = pd.DataFrame(columns=['Year', 'Trading Days', 'mu', 'sigma', '%% days < mu - 2 * sigma', '%% days > mu + 2 * sigma'])
    # Append each year to our dataframe
    for year in years:
        df_q3 = df_q3.append(create_daily_returns_with_std_deviation(df, year))
    print(df_q3)
    print('We expect that given a 2 tail standard deviation calculation, 2 standard deviations from the mean would yield about 2.5% per tail. The calculation shown above ')
    print('indicates that this is not the case. Each year has a significantly different percentages in its tails, usually with more in its left tail than its right tail. ')
    print('This suggests that there are significantly more "really bad trading days" than "really good trading days" indicating that bigger drops occur more frequently than ')
    print('bigger gains. On years with a high standard deviation of daily returns (eg. more volatile), namely 2015, 2016, and 2018, there is a significantly higher percentage of bad trading days ')
    print('compared to good ones: 3.17% vs 1.98%, 3.57% vs 0.79%, and 1.99% vs 0.8%. On years with high positive average returns, namely 2017, there is a higher percentage of "really good trading days" than "really bad trading days", but not by as much ')
    print('as the converse difference in 2015, 2016, and 2018. It seems as though generally, there are a higher percentage of big drops than big gains overall, and this is exacerbated by increased volatility (sigma) which deviates with majorly bullish years.')

if __name__ == "__main__":
    main()













