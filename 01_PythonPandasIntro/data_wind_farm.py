# -*- coding: utf-8 -*-

import os
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# global plotting options
matplotlib.style.use('ggplot')
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['axes.facecolor'] = 'silver'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams.update({'font.size': 18})


# configuration (for windows e. g. "C:\\IESMO\\data_wind_farm\\")
directory_path = ("/home/cord/Programmierung/IESMO/"
                  "Pandas_Example/data_wind_farm/")

# %% dataframe creation

# loop that reads excel files from folder
try:
    for file in os.listdir(directory_path):
        if file.endswith(".xls"):
            print("Converting: " + file)

            # read raw excel file and adjust columns/rows
            file_full_path = directory_path + file
            xlsx = pd.ExcelFile(file_full_path)

            # create temporary dataframe containing data for one file
            df_tmp = pd.read_excel(xlsx)

            # add column containing wea converter name (from file name)
            df_tmp['WEA'] = file.split("_", 1)[0]
            print(file.split("_", 1)[0])

            # rename created column (exemplary)
            df_tmp.rename(columns={'WEA': 'Wea'}, inplace=True)

            # drop columns that don't hold valuable data
            df_tmp.drop([col for col in ['WeaNr', 'Wpid']
                         if col in df_tmp.columns], inplace=True, axis=1)
            df_tmp.set_index(['Datumzeit'], inplace=True)

            # create dataframe that later on holds all values
            if 'df' not in globals():
                df = df_tmp
            else:
                df = pd.concat([df, df_tmp])
finally:
    print("All files have been converted.")


# %% indexing & slicing

# show size, index, column names, data types, ...
df.info()

# have a look at the first/last rows (compare with Spyder's variable browser)
df.head()
df.tail()

# show columns
df.columns

# show index
df.index

# sort index
df.sort_index(inplace=True)

# have another look
df.index

# there are different slicing options depending on the index and column type.
# here, we are slicing with a datetime index and labeled columns.
# for more information, see:
# http://pandas.pydata.org/pandas-docs/stable/indexing.html
# http://pandas.pydata.org/pandas-docs/stable/timeseries.html

# one day and one column
df['30/01/2001':'30/01/2001']['Wind']

# 30 minutes and two columns
df['01/01/2001 00:00:00':'01/01/2001 00:30:00'][['Wea', 'Leistung']]

# 30 minutes and two columns (sorted)
df['01/01/2001 00:00:00':'01/01/2001 00:30:00'][
    ['Wea', 'Leistung']].sort_values(by=['Wea'])

# one year and month
df['2002']
df['2002-6']

# two options for one month for one column
df.Wind['2002-6']
df['2002-6']['Wind']

# cleaning and reshaping a subset of the data from long to wide format
# see: http://pandas.pydata.org/pandas-docs/stable/reshaping.html
df_wind_wide = df[['Wea', 'Wind']]
df_wind_wide.head()
df_wind_wide.reset_index(inplace=True)
df_wind_wide = df_wind_wide.drop_duplicates(['Datumzeit', 'Wea'])
df_wind_wide.sort_values(by=['Wea', 'Datumzeit'], ascending=True, inplace=True)
df_wind_wide.set_index('Datumzeit', inplace=True)
df_wind_wide = df_wind_wide.pivot(index=None, columns='Wea', values='Wind')
df_wind_wide.head()

# save subset to csv file and read in back into a new dataframe
df_wind_wide.to_csv(directory_path + 'wind_farm.csv', sep=';', index=True,
                    header=True)
df_wind_wide_csv = pd.read_csv(directory_path + 'wind_farm.csv', sep=';')
df_wind_wide_csv.set_index('Datumzeit', inplace=True)

# check if old and new dataframes are identical and rename columns
df_wind_wide.equals(df_wind_wide_csv)

# rename columns
colnames = ['WEC1', 'WEC2', 'WEC3', 'WEC4', 'WEC5', 'WEC6']
df_wind_wide_csv.columns = colnames

# EXCERCISE 1 (15 minutes):
#
# create a csv file that contains the power output (Leistung) of the first
# three wind turbines in september 2003 (ordered by date in separate columns)
# and save it to your file system using a comma as delimiter


# %% basic statistics, resampling and subsetting

# show statistical parameters. which units to the columns probably have?
df.describe()

# get unique values for columns
df['Status'].unique()
df['Wind'].unique()

# create hourly wind speed series (note that the data type is a series (1D))
# what happened to the different turbines?
max_wind_speed_hourly = df['Wind'].resample('1H', how='max')
max_wind_speed_hourly.head()
max_wind_speed_hourly.shape

# let's find out which hours were stormy in ellhöft between 2001 and 2007
# http://www.wettergefahren.de/warnungen/windwarnskala.html
stormy_hours = max_wind_speed_hourly[(max_wind_speed_hourly >= 21)]
stormy_hours.head()
stormy_hours.shape

# EXCERCISE 2 (15 minutes):
#
# determine the number of days between 2001 and 2007 where at least one turbine
# of the wind farm had no feed-in (Leistung)

# %% basic plotting

# wind speed distribution (30 min mean) in Ellhöft in 2004
mean_wind_speed_30min = df[['Wind']].resample('30Min', how='mean')
mean_wind_speed_30min.head()
mean_wind_speed_30min['2004'].shape
hist = mean_wind_speed_30min['2004'].plot.hist(color='blue', bins=50,
                                               legend=False)
hist.set_title('Wind speed distribution')
hist.set_xlabel('Wind speed in m/s')
hist.set_ylabel('Frequency')

# wind speed (hourly mean) over time in 2004
df_wind_2004_hourly_mean = df_wind_wide['2004'].resample('H', how='mean')
line = df_wind_2004_hourly_mean.plot(kind='line', drawstyle='steps',
                                     subplots=True)
line[0].set_title('Wind speed in m/s')
line[5].set_xlabel('Date and time')
[item.legend(loc='upper right', fontsize=14) for item in line]

# basic plotting: annual production over time
# at first, the mean values per hour are calculated. afterwards, these are
# summed up on an annual basis
df_power_wide = df[['Wea', 'Leistung']]
df_power_wide.head()
df_power_wide.reset_index(inplace=True)
df_power_wide = df_power_wide.drop_duplicates(['Datumzeit', 'Wea'])
df_power_wide.sort_values(by=['Wea', 'Datumzeit'], ascending=True,
                          inplace=True)
df_power_wide.set_index('Datumzeit', inplace=True)
df_power_wide = df_power_wide.pivot(index=None, columns='Wea',
                                    values='Leistung')
df_power_wide.head()

df_prod_annual = df_power_wide.resample('1H', how='mean')
df_prod_annual = df_prod_annual.resample('1A', how='sum')
df_prod_annual.index = df_prod_annual.index.year
df_prod_annual = df_prod_annual.divide(10**3)
bar = df_prod_annual.transpose().plot(kind='bar', legend=True, rot=0)
bar.set_xlabel('Wind turbine')
bar.set_ylabel('Energy in MWh')
bar.legend(ncol=8)

# full load hours over time
# compare with: https://de.wikipedia.org/wiki/Volllaststunde
df_full_load_hours = df_prod_annual.divide(1.3)
bar = df_prod_annual.transpose().plot(kind='bar', legend=False, rot=0)
bar.set_xlabel('Wind turbine')
bar.set_ylabel('Full load hours')
bar.legend(ncol=8)

# EXCERCISE 3 (15 minutes):
#
# determine the annual earnings per turbine between 2001 and 2007 in Euro
# assuming a fixed feed-in price of 8.8 Ct/kWh and plot them using a bar chart.
#
# hint: use a suitable DataFrame method to obtain the result


# %% using functions

# create a new column by applying a function onto another function
def kw_in_mw(x):
    return x/1000

str(kw_in_mw)

df['Leistung_in_MW'] = df['Leistung'].apply(kw_in_mw)
df[['Leistung', 'Leistung_in_MW']].head()

# EXCERCISE 4 (20 minutes):
#
# calculate the power contained in the wind at each turbine and append the
# result as a new column. afterwards, look at the values for the first twenty
# day of april 2007 and find the turbine with the lowest value by applying
# a suitable dataframe method
#
# P_contained = 1/2 * roh_air * A * v_wind^3
#
# roh_air = air density of 1.188 kg/m^3 at 20°C (vgl. Quasching, 2005)
# A = airflow area (rotor diameter is 62 m) in m^2
# v_wind = wind speed at hub height in m/s
#
# hint: use python's integrated math package where possible
#       (https://docs.python.org/3/library/math.html)
