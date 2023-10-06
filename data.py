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

def extract_single_year_remove_mean(year, data):
    year_string_start = str(year)+"0101"
    year_string_end = str(year)+"1231"
    year_data = data.loc[year_string_start:year_string_end, ['Tide']]
    # remove mean to oscillate around zero
    mmm = np.mean(year_data['Tide'])
    year_data['Tide'] -= mmm

    return year_data


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
ax.set_xlim([datetime.date(2008, 1, 1), datetime.date(2008, 12, 31)])
fig_summary.tight_layout()

FD_2008 = extract_single_year_remove_mean(2008, Fort_Denison)
BI_2008 = extract_single_year_remove_mean(2008, Booby_Island)
F_2008 = extract_single_year_remove_mean(2008, Freemantle)

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

# gives 0.053m for M2. Actual is 0,052m

seconds_since = (FD_2008.index.astype('int64').to_numpy()/1e9) - datetime.datetime(2008,1,1,0,0,0).timestamp()
amp,pha = uptide.harmonic_analysis(tide, FD_2008['Tide'].to_numpy()/1000, seconds_since)


seconds_since = (BI_2008.index.astype('int64').to_numpy()/1e9) - datetime.datetime(2008,1,1,0,0,0).timestamp()
amp,pha = uptide.harmonic_analysis(tide, BI_2008['Tide'].to_numpy()/1000, seconds_since)

seconds_per_day = 24*60*60

import pytz
tz = pytz.timezone("Australia/Sydney")
tide.set_initial_time(datetime.datetime(2008,1,1,0,0,0))
seconds_since = (FD_2008.index.astype('int64').to_numpy()/1e9) - datetime.datetime(2008,1,1,0,0,0,tzinfo=tz).timestamp()


constituents  = ['M2', 'S2', 'N2', 'K2', 'O1', 'P1', 'Q1', 'M4']
print(uptide.select_constituents(constituents,15*24*60*60))
tide = uptide.Tides(['K1', 'O1'])
print(tide.get_minimum_Rayleigh_period()/86400.)
tide = uptide.Tides(['K1', 'M2'])
print(tide.get_minimum_Rayleigh_period()/86400.)


tide = uptide.Tides(['M2'])
tide.set_initial_time(datetime.datetime(2008,1,1,0,0,0))
amp = [0.50125979]
pha = [4.18331822]

t = np.arange(0, 365*24*3600, 600)
eta = tide.from_amplitude_phase(amp, pha, t)
fig_summary=plt.figure()
ax=fig_summary.add_subplot(111)
fd = ax.plot(seconds_since, FD_2008['Tide']/1000, color="blue", lw=1, label="Fort Denison")
bi = ax.plot(t, eta, color="orange", lw=1, label="M2 only")
ax.set_xlabel("Date")
ax.set_ylabel("Water height (mm)")
ax.tick_params(axis='x', rotation=45)
ax.set_xlim([0, 14*24*60*60])
ax.legend()
#ax.set_xlim([datetime.date(2008, 6, 1), datetime.date(2008, 7, 1)])
fig_summary.tight_layout()

# add S2, K1, O1



# Then add model data:


