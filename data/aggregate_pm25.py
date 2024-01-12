import pandas as pd
from pathlib import Path
import numpy as np

data_dir = Path(r"C:\Users\Nick\src\goldenair\data")

pa = Path(data_dir, "purpleair", "download_tool", "purpleair.csv")

aqi = pd.read_csv(pa, index_col=0, parse_dates=True)
aqi.index = aqi.index.tz_convert('Canada/Mountain')
aqi.station = aqi.station.astype('str')

# filter outrageous data values
for measure in ['pm2.5_atm', 'pm2.5_alt', 'pm2.5_cf_1']:
    aqi.loc[aqi[measure] > 500, measure] = np.nan

met = pd.read_csv(r"C:\Users\Nick\src\goldenair\data\weather\meteo.csv", low_memory=False)
met.index = pd.to_datetime(met['time'])
met.index = met.index.tz_localize("Canada/Mountain",nonexistent='NaT', ambiguous='NaT')

cols = ['temp', 'temp_dew', 'wind_dir', 'wind_spd', 'hmdx', 'precip_amt','pressure', 'rel_hum']
average_met = met.groupby(met.index)[cols].mean()
average_met.resample('H').mean()

df = average_met.join(aqi, how='inner')

df.to_csv(Path(data_dir, "aggregated_long.csv"))

df = df[df.index.month.isin([10,11,12,1,2,3,])
parson = df[df['station']=='47891']
matt = df[df['station']=='127469']
meg = df[df['station']=='100155']

measure = 'pm2.5_atm'
plt.plot(parson.groupby(parson.index.hour)[measure].mean())
plt.plot(matt.groupby(matt.index.hour)[measure].mean())
plt.plot(meg.groupby(meg.index.hour)[measure].mean())
plt.hlines(27, 0,24, linestyles='dashed')
plt.show()

met[met['station_id']==54318]['temp'].groupby(met[met['station_id']==54318].index.hour).mean().plot(label='GOLDEN AIRPORT 54318')
met[met['station_id']==52980]['temp'].groupby(met[met['station_id']==52980].index.hour).mean().plot(label = 'GOLDEN A 52980')
met[met['station_id']==1364]['temp'].groupby(met[met['station_id']==1364].index.hour).mean().plot(label='GOLDEN A 1364')
plt.legend()
plt.show()

plt.plot(aqi.loc[aqi['station']=='47891','pm2.5_alt']);plt.show()

parson['pm2.5_alt'].rolling('24H').mean().groupby(parson.index.dayofyear).mean().plot();plt.show()

x = df[['station', 'pm2.5_alt']].reset_index().set_index(['time', 'station']).unstack()
x.columns = [c[1] for c in x.columns]
x = x[x.index.month.isin([9,10,11,12,1,2,3,4])]

def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, '--')

