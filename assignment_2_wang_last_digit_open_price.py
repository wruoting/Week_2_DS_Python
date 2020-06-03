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


def list_all_open_days_by_cent(df, year_start, year_end):
    """
    df: pd dataframe. Data of interest
    year_start: int/string. The start year
    year_end: int/string. The end year 
    returns: Series with unique sort day counts
    """
    year_start = str(year_start)
    year_end = str(year_end)
    # Return is calculated as a percentage, eg. 0.3 -> 0.3%
    start_date=year_start + '-01-01'; 
    end_date=year_end + '-12-31'
    df_returns = df.loc[((df['Date'] >= start_date) & (df['Date'] <= end_date))].copy()
    # This ensures that we will only get 2
    open_days = np.round(df_returns['Open'], 2)
    # All "cent" digits for the open days; multiply by 100 and mod by 10. Convert to int to sort by
    cent_days = np.remainder(np.multiply(open_days, 100), 10).astype('int64')
    # Sort the days
    unique_sort_day_counts = pd.Series('Frequencies', index = ['Digit'])
    unique_sort_day_counts = unique_sort_day_counts.append(cent_days.value_counts(sort=True))
    return unique_sort_day_counts

def max_absolute_error(actual_vector, prediction_vector):
    """
    actual_vector: vector for actual data
    prediction_vector: vector for prediction data
    return: float for the absolute error
    """
    # Find the max of the absolute value of the difference between the prediction and absolute vector
    # For actual_vector = a1, a2, ... an and prediction_vector p1, p2, ... pn
    # The error is calculated as: max(|a1-p1|, |a2-p2|, ...., |an-pn|)
    vector_diff = np.subtract(actual_vector, prediction_vector)
    abs_vector_diff = np.abs(vector_diff)
    return np.round(np.max(abs_vector_diff), 5)


def median_absolute_error(actual_vector, prediction_vector):
    """
    actual_vector: vector for actual data
    prediction_vector: vector for prediction data
    return: float for the absolute error
    """
    # Find the median_absolute_error of the absolute value of the difference between the prediction and absolute vector
    # For actual_vector = a1, a2, ... an and prediction_vector p1, p2, ... pn
    # The error is calculated as: median_absolute_error(|a1-p1|, |a2-p2|, ...., |an-pn|)
    vector_diff = np.subtract(actual_vector, prediction_vector)
    abs_vector_diff = np.abs(vector_diff)
    return np.round(np.median(abs_vector_diff), 5)

def mean_absolute_error(actual_vector, prediction_vector):
    """
    actual_vector: vector for actual data
    prediction_vector: vector for prediction data
    return: float for the absolute error
    """
    # Find the mean_absolute_error of the absolute value of the difference between the prediction and absolute vector
    # For actual_vector = a1, a2, ... an and prediction_vector p1, p2, ... pn
    # The error is calculated as: 1/N * sum from i=1 to n : |ai-pi|
    vector_diff = np.subtract(actual_vector, prediction_vector)
    abs_vector_diff = np.abs(vector_diff)
    total_sum = np.sum(abs_vector_diff)
    size = np.size(vector_diff)
    mean_calculation = np.divide(total_sum ,size)
    return np.round(mean_calculation, 5)

def root_mean_squared_error(actual_vector, prediction_vector):
    """
    actual_vector: vector for actual data
    prediction_vector: vector for prediction data
    return: float for the RMSE
    """
    # Find the mean_absolute_error of the absolute value of the difference between the prediction and absolute vector
    # For actual_vector = a1, a2, ... an and prediction_vector p1, p2, ... pn
    # The error is calculated as: sqrt(1/N * sum from i=1 to n : (ai-pi)^2)
    vector_diff = np.subtract(actual_vector, prediction_vector)
    abs_vector_diff = np.abs(vector_diff)
    abs_vector_diff_squared = np.square(abs_vector_diff)
    total_sum = np.sum(abs_vector_diff_squared)
    size = np.size(vector_diff)
    mean_calculation = np.divide(total_sum ,size)
    rmse = np.sqrt(mean_calculation)
    return np.round(rmse, 5)

def create_table_by_years(df, start_year, end_year):
    """
    df: pd dataframe. Data of interest
    year_start: int/string. The start year
    year_end: int/string. The end year 
    returns: Table with years and corresponding method of error
    """
    year_range = range(start_year, end_year+1)
    prediction_vector = np.full(10, 0.1)
    dict_of_years_and_calculations = {}
    for year in year_range:
        frequencies = list_all_open_days_by_cent(df, year, year)
        # Create the actual vector
        actual_vector_values = np.array(frequencies[1:].sort_index())
        sum_vector = np.sum(actual_vector_values)
        # Convert this vector into percentages
        actual_vector_percentages = np.divide(actual_vector_values, sum_vector)
        dict_of_years_and_calculations[year] = np.array([max_absolute_error(actual_vector_percentages, prediction_vector),
            median_absolute_error(actual_vector_percentages, prediction_vector),
            mean_absolute_error(actual_vector_percentages, prediction_vector),
            root_mean_squared_error(actual_vector_percentages, prediction_vector)])
   
    return pd.DataFrame.from_dict(dict_of_years_and_calculations, orient='index', columns = ['Max Absolute Error', 'Median Absolute Error', 'Mean Absolute Error', 'Root Mean Squared Error']).T

def main():
    df = pd.read_csv(ticker_file)
    years = range(2014, 2019)
    # Create a frequencies series
    frequencies = list_all_open_days_by_cent(df, 2014, 2018)
    prediction_vector = np.full(10, 0.1)
    # Create the actual vector
    actual_vector_values = np.array(frequencies[1:].sort_index())
    sum_vector = np.sum(actual_vector_values)
    # Convert this vector into percentages
    actual_vector_percentages = np.divide(actual_vector_values, sum_vector)

    # Print the frequencies table
    print('Data from 2014 to 2018')
    print(frequencies)
    print('2014 Data')
    print(list_all_open_days_by_cent(df, 2014, 2014))
    print('2015 Data')
    print(list_all_open_days_by_cent(df, 2015, 2015))
    print('2016 Data')
    print(list_all_open_days_by_cent(df, 2016, 2016))
    print('2017 Data')
    print(list_all_open_days_by_cent(df, 2017, 2017))
    print('2018 Data')
    print(list_all_open_days_by_cent(df, 2018, 2018))
    print('------------------------------------------')
    print('Question 1: ')
    print('The most frequent digit from 2014 to 2018 is 0.')
    print('The most frequent digit for 2014 is 8.')
    print('The most frequent digit for 2015 is 0.')
    print('The most frequent digit for 2016 is 0.')
    print('The most frequent digit for 2017 is 0.')
    print('The most frequent digit for 2018 is 0.')
    print('Question 2: ')
    print('The least frequent digit from 2014 to 2018  is 2.')
    print('The least frequent digit for 2014 is 2.')
    print('The least frequent digit for 2015 is 7.')
    print('The least frequent digit for 2016 is 7.')
    print('The least frequent digit for 2017 is 2.')
    print('The least frequent digit for 2018 is 8.')
    print('Question 3: Errors are calculated as an absolute error, not a percentage error. Multiply by 100 to get percentage error')
    print('Calculations are for all 4 years')
    print('(a) Max Absolute Error')
    print(max_absolute_error(actual_vector_percentages, prediction_vector))
    print('(b) Median Absolute Error')
    print(median_absolute_error(actual_vector_percentages, prediction_vector))
    print('(c) Mean Absolute Error')
    print(mean_absolute_error(actual_vector_percentages, prediction_vector))
    print('(d) Root Mean Squared Error')
    print(root_mean_squared_error(actual_vector_percentages, prediction_vector))
    print('Calculations for each individual year is listed below')
    print(create_table_by_years(df, 2014, 2018))
    print('For the most frequent digit, it seems that there is a consistent last digit opening price frequency of 0 throughout the four years of 2014 to 2018. Benford\'s law does not extend to 0, ')
    print('but it could provide a possible explanation for the increased frequency of 0 since it is the lowest possible digit here. The distribution described by Benford\'s law does not seem to apply here.')
    print('A possible explanation could also be that first orders of the day will generally round to 0. The least digit does not seem to be consistent throughout the years, but there is a frequency between 2, 7, and 8.')
    print('Max absolute error between predicted uniform distribution of 10% per digit remains approximately 5% throughout 2015 and 2017 but varies for 2014 and 2018. It looks like 2018 saw an increased rise in the 0 digit ')
    print('in frequency, which results in the greater error in that year overall for max, median, mean, and RMS error. For median error, the difference was miniscule between the years, from 1.4% to 2.6% difference. The mean ')
    print('and RMSE also don\'t show significant differences across the 4 years except for 2018, which has the greatest error in both those categories. ')


if __name__ == "__main__":
    main()













