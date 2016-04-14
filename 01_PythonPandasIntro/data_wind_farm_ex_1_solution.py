# -*- coding: utf-8 -*-

# EXCERCISE 1 (15 minutes):
#
# create a csv file that contains the power output of the first three wind
# turbines in september 2003 (ordered by date in separate columns) and save
# it to your file system using a comma as delimiter


df_power_2002_9_wide = df['2002-9'][['Wea', 'Leistung']]
df_power_2002_9_wide.reset_index(inplace=True)
df_power_2002_9_wide.sort_values(by=['Wea', 'Datumzeit'], ascending=True,
                                 inplace=True)
df_power_2002_9_wide.set_index('Datumzeit', inplace=True)
df_power_2002_9_wide = df_power_2002_9_wide.pivot(index=None, columns='Wea',
                                                  values='Leistung')
df_power_2002_9_wide = df_power_2002_9_wide[['WKA1', 'WKA2', 'WKA3']]
df_power_2002_9_wide.to_csv('wind_farm_2002_9_t123.csv', sep=',', index=True,
                            header=True)
df_power_2002_9_wide.head()
