import pandas as pd
import matplotlib.pyplot as plt

def winter(df, winter_start=305, winter_end=90):
    return (df.index.dayofyear < winter_end) | (df.index.dayofyear > winter_start)

def summer(df, winter_start=305, winter_end=90):
    return (df.index.dayofyear > winter_end) & (df.index.dayofyear < winter_start)

# how well does venting index predict air quality?
vi = pd.read_csv(r"C:\Users\Nick\src\goldenair\VI\venting_index.csv", index_col=0, parse_dates=True)
vi_daily = vi['VI'].resample('D').mean()

aqi = pd.read_csv(r"C:\Users\Nick\src\goldenair\data\purpleair\download_tool\47891_Parson_house_2015-01-01 2023-01-01 60-Minute Average.csv", index_col=0, parse_dates=True)
aqd = aqi['pm2.5_atm'].copy()
aqd.dropna(inplace=True)
aqd = aqd.resample('D').mean()
aqd.index = aqd.index.tz_localize(None)  # TODO: first convert to mtn time zone!
# 
df = pd.merge(vi_daily, aqd, left_index=True, right_index=True)
df.dropna(inplace=True)

df = df[(df.index.dayofyear < 90) | (df.index.dayofyear > 305)]

fig, ax = plt.subplots()
ax.plot(df['VI'].values, df['pm2.5_alt'].values, '.')
ax.set_xlabel("Daily Mean Venting Index")
ax.set_ylabel("Daily mean PM2.5 [$\mu g/m^3$]")
fig.show()

# how well does temperature predict air quality?
meteo = pd.read_csv(r"C:\Users\Nick\src\goldenair\weather\meteo.csv",  parse_dates=False, low_memory=False)
met = meteo.drop(meteo.columns[0], axis=1)
met.index = pd.DatetimeIndex(pd.to_datetime(meteo['time']))
met_airport = met.groupby('station_id').get_group(54318)

met_daily_T = met_airport['temp'].resample('D').mean()

temp = meteo[['time','temp']].copy()
temp.dropna(inplace=True)
temp = temp.groupby('time').mean()
temp.index = pd.DatetimeIndex(pd.to_datetime(temp.index))
tempd = temp.resample('D').mean()
df = pd.merge(tempd, aqd, left_index=True, right_index=True)

fig, ax = plt.subplots()
ax.plot(df['temp'].values[winter(df)], df['pm2.5_alt'].values[winter(df)], '.')
ax.set_xlabel("Daily Mean Air Temperature")
ax.set_ylabel("Daily mean PM2.5 [$\mu g/m^3$]")
fig.show()


plt.plot(aqi['pm2.5_alt'], aqi['pm2.5_cf_1'], '.');plt.show()

local = aqi.drop(['station'], axis=1)[aqi['station']==47891]

