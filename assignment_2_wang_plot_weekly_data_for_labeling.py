# -*- coding: utf-8 -*-
"""
@author: rwang
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ticker='WMT'

ticker_file = './{}_Labeled.csv'.format(ticker)
plot_dir = './{}-plots.csv'.format(ticker)

# This file is meant to visualize the volume and price movement for all the days in the file named
# {ticker-name}_Labled.csv. In this example, it is WMT_Labeled

try:   
    df = pd.read_csv(ticker_file)
    total_week_years = df['Year_Week'].unique()
    # For file name sake we replace / with _
    start_date = df['Date'].iloc[0].replace('/', '_')
    end_date = df['Date'].iloc[-1].replace('/', '_')
    output_file = os.path.join(start_date + '_to_' + end_date  + '_prices_' + ticker +  '.pdf')
    pdf = PdfPages(output_file)

    for index, week in enumerate(total_week_years):
        # Grab the week matching
        df_week = df[df['Year_Week'] == week]
        df_week = df_week[['Date','Week_Number','Weekday', 'Day', 'Volume', 'Close']]
        weekday_list = df_week['Weekday'].tolist()
        ticks_list = df_week['Date'].tolist()
        start_date = df_week['Date'].iloc[0].replace('/', '_')
        end_date = df_week['Date'].iloc[-1].replace('/', '_')

        fig, ax1 = plt.subplots()

        color = 'tab:blue'
        ax1.set_xlabel('Volume')
        ax1.set_ylabel('Volume', color=color)
        ax1.bar(df_week['Date'],  df_week['Volume'], color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:red'
        ax2.set_ylabel('Close Price', color=color)
        ax2.plot(df_week['Date'], df_week['Close'], color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        plt.grid(True)
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title('Daily prices for ' + ticker +  ' from ' + start_date + ' to ' + end_date)
        pdf.savefig(fig)
        plt.close()
        print('Saving Week {} of {}'.format(index+1, len(total_week_years)))
    pdf.close()

except Exception as e:
    print('An error occured for ticker: {} with exception : {}'.format(ticker, e))
