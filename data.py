
import pandas as pd

Fort_Denison = pd.read_csv("h333.csv", header=None)
Fort_Denison['Date'] = pd.to_datetime(dict(year=Fort_Denison[0], month=Fort_Denison[1], day=Fort_Denison[2], hour=Fort_Denison[3]))
# col 0 is year, col 1 is month, col2 is day, col3 hour
Fort_Denison = Fort_Denison.drop([0,1,2,3], axis = 1)
Fort_Denison = Fort_Denison.rename(columns={4: "Tide"})
Fort_Denison = Fort_Denison.set_index('Date')
Fort_Denison = Fort_Denison.mask(Fort_Denison['Tide'] < -300)
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
