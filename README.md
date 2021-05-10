	This python project uses web scraping to obtain raw spectral wave data from
https://www.ndbc.noaa.gov/ . The data for a NOAH buoy is scraped using the BeautifulSoup library
and formatted into a DataFrame using the pandas library. The raw data is converted from
a string to a list of lists and from there to various types including int, float, 
and a datetime object. Wave height rows within the previous specificed amount 
of days (currently 5) are then selected from the DataFrame and plotted against the 
date and time on the x axis. This project's functional approach makes it easy to 
incorporate new data and other metrics from the spectral wave data as well as 
other buoys all over the world.
