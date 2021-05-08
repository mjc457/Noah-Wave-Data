import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
#%matplotlib inline since not using jupyter notebook
import re
import time
from datetime import datetime
# import matplotlib.dates as mdates
# import matplotlib.ticker as ticker
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

from bokeh.plotting import figure, show, gridplot
# from bokeh.models import ColumnDataSource
# from bokeh.transform import dodge
# import math
# from bokeh.io import curdoc
# curdoc().clear
# from bokeh.io import push_notebook, show, output_notebook
# from bokeh.layouts import row
# from bokeh.plotting import figure
# from bokeh.transform import factor_cmap
# from bokeh.models import Legend
# output_notebook()

import datetime
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
#warnings.warn(msg, FutureWarning)

"""
    all imports of matplotlib and seaborn are giving error:
    Unable to init server: Could not connect: Connection refused
Unable to init server: Could not connect: Connection refused
(44065.py:82): Gdk-CRITICAL **: 20:01:25.111: gdk_cursor_new_for_display: assertion 'GDK_IS_DISPLAY (display)' failed
"""
def get_buoy_data(buoy):
    """
        pulls data from specific buoy number and returns raw data
        PARAMETERS:
                   buoy - int - number of noah buoy
       RETURN:
                   bs4.element.tag
    """  
    #https://www.ndbc.noaa.gov/data/realtime2/44065.spec this is page for 44065 with tabular data
    #Define a user-agent which will help in bypassing the detection as a scraper
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    
    #Extract the content from requests.get
    #Specify the URL to requests.get and pass the user-agent header as an argument
    
    
    r = requests.get('https://www.ndbc.noaa.gov/data/realtime2/' + str(buoy) + '.spec', headers = headers)#, proxies=proxies)
    content = r.content
    
    #Scrape the specified page and assign it to soup variable
    soup = BeautifulSoup(content, features = "lxml")
    unorganized_raw_data = soup.find('p')
    
    return unorganized_raw_data                             # returns a bs4.element.tag of the NOAH webpage raw spectral wave data
    
    
    # # make each line its own list with each whitespace delimited substring its own element.
    # for line in data.text.split('\n'):                      # split string on new line and make list
        # if line:                                            # if the list is not empty, add it to buoy_data list
            # buoy_data.append(line.split())                  # add each line list to buoy_data list and split each line so every whitespace delimited substring is its own element

    # return buoy_data                                        # returns a list of lists NOTE THAT ALL ELEMENTS ARE STRINGS
""" ####################################################################################################### """




#call this function with return from get_buoy_data()
"""######################################################################################################"""
def organize_raw_data(data):
    """
        organizes raw_data (in form of bs4.element.tag '<p>') from specific buoy number
        
        PARAMETERS:
                    data - takes in raw_unorganized_data in form of bs4.element.tag ('<p>')  
        RETURN:     buoy_data - a list of lists
    """
    
    #list to be made into dataframe
    buoy_data = []
    
    # make each line its own list with each whitespace delimited substring its own element.
    for line in data.text.split('\n'):                      # split string on new line and make each line a list
        if line:                                            # if the list (line) is not empty, add it to buoy_data list
            buoy_data.append(line.split())                      # add each line list to buoy_data list and split each line so every whitespace delimited substring is its own element

    return buoy_data                                        # returns a list of lists NOTE THAT ALL ELEMENTS ARE STRINGS    
""" ####################################################################################################"""




# calling this function with return from make_buoy_dataframe(raw_data)
""" ####################################################################################################"""
def make_buoy_dataframe(raw_data):
    """
        takes a list of buoy data and makes it into an organized dataframe
        PARAMETERS:
                   buoy - int - number of noah buoy
        RETURN:
               df - dataframe of organized buoy data with datetime information organized
    """
    column_header = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'WVHT', 'SwH','SwP', 'WWH', 'WWP', 'SwD', 'WWD', 'STEEPNESS', 'APD', 'MWD']       

    # make pandas dataframe                                              
    df = pd.DataFrame(raw_data, columns = column_header)
    df = df.drop([0, 1])                        # remove first two rows containing column names and units respectively. This also shifts row indexes iloc is 0 based integer position 
    df.reset_index(drop = True, inplace = True)              #dataframe with first row removed and row index restarted from '0'
    df.replace('MM', '-99', inplace = True)     #all dtypes are currently strings (objects) MM is can be used from NOAH webpage to fill an element with no data
    #change 'YEAR', 'Month', 'Day', 'Hour', 'Minute', 'MWD' to int
    df['Year'] = pd.to_numeric(df['Year'])
    df['Month'] = pd.to_numeric(df['Month'])
    df['Day'] = pd.to_numeric(df['Day'])
    df['Hour'] = pd.to_numeric(df['Hour'])
    df['Minute'] = pd.to_numeric(df['Minute'])
    df['MWD'] = pd.to_numeric(df['MWD'])

    #Make Date column and format Year, Month, Day, Hour, Minute then remove these added individual columns
    #  datetime.datetime(year, month, day, hour, minute)
    date = []
    for ind in df.index:
         date.append(datetime.datetime(df['Year'][ind], df['Month'][ind], df['Day'][ind], df['Hour'][ind], df['Minute'][ind]))
         
    df['Date'] = date       # adding new column to dataframe using 'Date' as the column name and equating it to the list
    df.drop(['Year', 'Month', 'Day', 'Hour', 'Minute'], axis = 'columns', inplace = True)

    #change 'WVHT', 'SwH','SwP', 'WWH', 'WWP, and APD to float
    df['WVHT'] = pd.to_numeric(df['WVHT'])
    df['SwH'] = pd.to_numeric(df['SwH'])
    df['SwP'] = pd.to_numeric(df['SwP'])
    df['WWH'] = pd.to_numeric(df['WWH'])
    df['WWP'] = pd.to_numeric(df['WWP'])
    df['APD'] = pd.to_numeric(df['APD'])

    # REPLACE '-99 WITH nan' for both string (obejct) type, and int and float type
    df.replace(str(-99), np.nan, inplace = True)
    df.replace(-99, np.nan, inplace = True)
    
    return df
"""################################################################################################################"""

   



"""#####################################################################################################################""" 
def wvht_vs_time_x_days(df, x):
    """
        makes a dataframe containing the date and SWHT. removes all 'nAn' values
        PARAMETERS: df - dataframe with full buoy data
                    x - int - number of previous days to keep in new dataframe subset
        RETURN:     a dataframe subset with swell height and datetime date.  all nan values removed for these two columns
    """
    current_date= df['Date'].iloc[0]
    x_days_ago = current_date - datetime.timedelta(days = x)
    df.drop(['SwH', 'SwP', 'WWH', 'WWP', 'SwD', 'WWD', 'STEEPNESS', 'APD', 'MWD'], axis = 1, inplace = True)
    df.dropna(inplace = True)
    return df[df['Date'] >= x_days_ago]
"""#####################################################################################################################"""    



"""#####################################################################################################################"""
def thin_data(df, x):
      """
        takes a dataframe and returns every xth row
        PARAMETERS: df - dataframe
                    x - int - take every xth row of data
        RETURN:     a dataframe subset with only every xth row
      """
      return df.iloc[0::5, :]                  # start at 0th row select every 5th row of data, select all columns        

"""#####################################################################################################################"""
#pd.set_option("display.max_rows", None, "display.max_columns", None)    #prints all rows and columns
buoy_44065 = get_buoy_data(44065)
organized_buoy_44065 = organize_raw_data(buoy_44065)
df_44065 = make_buoy_dataframe(organized_buoy_44065)

#buoy 44025
buoy_44025 = get_buoy_data(44025)
organized_buoy_44025 = organize_raw_data(buoy_44025)
df_44025 = make_buoy_dataframe(organized_buoy_44025)


#New wvht and datetime time subset dataframes for each respective buoy
wvht_44065 = thin_data(wvht_vs_time_x_days(df_44065, 5), 5)
wvht_44025 = thin_data(wvht_vs_time_x_days(df_44025, 5), 5)



p_44065 = figure(title = "NOAH Buoy 44065 Swell Height vs Time for 5 Day Period", x_axis_label = 'Date', y_axis_label = 'Swell Height(meters)', x_axis_type = 'datetime')
p_44025 = figure(title = "NOAH Buoy 44025 Swell Height vs Time for 5 Day Period", x_axis_label = 'Date', y_axis_label = 'Swell Height(meters)', x_axis_type = 'datetime')
p_44065.title.align = 'center'
p_44025.title.align = 'center'
#vertical bars
p_44065.vbar(x = wvht_44065['Date'], top = wvht_44065['WVHT'], width = 0.5, bottom = 0, color = 'red')
p_44025.vbar(x = wvht_44025['Date'], top = wvht_44025['WVHT'], width = 0.5, bottom = 0, color = 'green')
g = gridplot([[p_44065, p_44025], [None, None]])
show(g)