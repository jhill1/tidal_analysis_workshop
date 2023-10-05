import pandas as pd
import matplotlib.pyplot as plt
import datetime
import wget
import os
import numpy as np

FortDenison_url = "https://uhslc.soest.hawaii.edu/data/csv/fast/hourly/h333.csv"
BoobyIsland_url = "https://uhslc.soest.hawaii.edu/data/csv/fast/hourly/h336.csv"
Freemantle_url = "https://uhslc.soest.hawaii.edu/data/csv/fast/hourly/h175.csv"
urls = [FortDenison_url, BoobyIsland_url, Freemantle_url]

def read_and_process_data(filename):
    tide_data = pd.read_csv(filename, header=None)
    tide_data['Date'] = pd.to_datetime(dict(year=tide_data[0], month=tide_data[1], day=tide_data[2], hour=tide_data[3]))
    # col 0 is year, col 1 is month, col2 is day, col3 hour
    tide_data = tide_data.drop([0,1,2,3], axis = 1)
    tide_data = tide_data.rename(columns={4: "Tide"})
    tide_data = tide_data.set_index('Date')
    tide_data = tide_data.mask(tide_data['Tide'] < -300)

    return tide_data

# fetch our data and store
for url in urls:
    file_name = os.path.basename(url) # get the full path to the file
    if os.path.exists(file_name):
        os.remove(file_name) # if exists, remove it directly
    file_name = wget.download(url, out=".")
    

Fort_Denison = read_and_process_data("h333.csv")
Booby_Island = read_and_process_data("h336.csv")
Freemantle = read_and_process_data("h175.csv")


fig_summary=plt.figure()
ax=fig_summary.add_subplot(111)
fd = ax.plot(Fort_Denison['Tide'], color="blue", lw=1, label="Fort Denison")
bi = ax.plot(Booby_Island['Tide'], color="orange", lw=1, label="Booby_Island")
f = ax.plot(Freemantle['Tide'], color="red", lw=1, label="Freemantle")
ax.set_xlabel("Date")
ax.set_ylabel("Water height (mm)")
ax.tick_params(axis='x', rotation=45)
ax.legend()
ax.set_xlim([datetime.date(2008, 6, 1), datetime.date(2008, 7, 1)])
fig_summary.tight_layout()

FD_2008 = Fort_Denison.loc['20080101':'20081231', ['Tide']]
BI_2008 = Booby_Island.loc['20080101':'20081231', ['Tide']]
F_2008 = Freemantle.loc['20080101':'20081231', ['Tide']]
# remove mean to oscillate around zero
mmm = np.mean(FD_2008['Tide'])
FD_2008['Tide'] -= mmm
mmm = np.mean(BI_2008['Tide'])
BI_2008 -= mmm
mmm = np.mean(F_2008['Tide'])
F_2008 -= mmm

fig_summary=plt.figure()
ax=fig_summary.add_subplot(111)
fd = ax.plot(FD_2008['Tide'], color="blue", lw=1, label="Fort Denison")
bi = ax.plot(BI_2008['Tide'], color="orange", lw=1, label="Booby_Island")
f = ax.plot(F_2008['Tide'], color="red", lw=1, label="Freemantle")
ax.set_xlabel("Date")
ax.set_ylabel("Water height (mm)")
ax.tick_params(axis='x', rotation=45)
ax.legend()
ax.set_xlim([datetime.date(2008, 6, 1), datetime.date(2008, 7, 1)])
fig_summary.tight_layout()


import uptide
tide = uptide.Tides(['M2'])



tide.set_initial_time(datetime.datetime(2008,1,1,0,0,0))
seconds_since = (F_2008.index.astype('int64').to_numpy()/1e9) - datetime.datetime(2008,1,1,0,0,0).timestamp()
amp,pha = uptide.harmonic_analysis(tide, F_2008['Tide'].to_numpy()/1000, seconds_since)

# give 0.053m for M2. Actual is 0,052m

seconds_since = (FD_2008.index.astype('int64').to_numpy()/1e9) - datetime.datetime(2008,1,1,0,0,0).timestamp()
amp,pha = uptide.harmonic_analysis(tide, FD_2008['Tide'].to_numpy()/1000, seconds_since)


seconds_since = (BI_2008.index.astype('int64').to_numpy()/1e9) - datetime.datetime(2008,1,1,0,0,0).timestamp()
amp,pha = uptide.harmonic_analysis(tide, BI_2008['Tide'].to_numpy()/1000, seconds_since)


import pytz
tz = pytz.timezone("Australia/Sydney")
tide.set_initial_time(datetime.datetime(2008,1,1,0,0,0))
seconds_since = (BI_2008.index.astype('int64').to_numpy()/1e9) - datetime.datetime(2008,1,1,0,0,0,tzinfo=tz).timestamp()



# wget data
# munge dates (need function to do this; create module for common crap like this)
# plot
# plot subset
# do same for other data
# plot each station as sep line for same dates

# analysis:
#   - use 40 days
#   - remove linear trend
#   - plot
#   - calculate Rayleigh
#   - extract a single consist
#   - plot and compare to real signal
#   - extract multiple and compare
#   - Do same for longer data period (e.g. year)
