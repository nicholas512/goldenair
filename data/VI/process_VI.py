from collections import namedtuple
from datetime import datetime
from pathlib import Path
import re
import pandas as pd


I = namedtuple("VentingForecast", ['date', 'time', 'VI', 'VItext', 'wnd', 'mxgHt'])

def get_venting(file):
    with open(file) as f:
        lines = f.readlines()
    
    # read date
    strdate = None
    while not strdate:
        line = lines.pop(0)
        if re.match(r"^\d\d-[^-]*-\d\d\d\d", line.strip()):
            strdate = line.strip()

    L = None
    while not L:
        line = lines.pop(0)
        if re.match(r"^GOLDEN", line.strip()):
            L = line.strip().split()

    f7 = I(strdate, "07:00", *L[1].split("/"), L[2], L[3])
    f16 = I(strdate, "16:00", *L[4].split("/"), L[5], L[6])
    
    return [f7, f16]

# datetime.strptime("05-JANUARY-2010", "%d-%B-%Y")

v = get_venting(r"C:\Users\Nick\src\goldenair\data\VI\2010\EC_BBS_100103_Sun_January_03_10.txt")

files = Path(r"C:\Users\Nick\src\goldenair\data\VI").glob("**/*.txt")

forecasts = []

for f in files:
    print(f)
    try:
        v = get_venting(f)
    except IndexError:
        print("nodata")
    forecasts += v

# convert to dataframe

df = pd.DataFrame.from_records(forecasts, columns =I._fields)

# clean up
df.index = pd.DatetimeIndex(pd.to_datetime(df['date'] +"T"+ df['time'], format="%d-%B-%YT%H:%M"))
df = df.sort_index(ascending=True)
df['VI'] = df['VI'].astype(float)
df['wnd'] = df['wnd'].astype(float)
df['mxgHt'] = df['mxgHt'].astype(float)

df.drop(df.index[df.index.year<2000], inplace=True)

df.to_csv(r"C:\Users\Nick\src\goldenair\data\VI\venting_index.csv")

import matplotlib.pyplot as plt
plt.plot(df['VI'].iloc[5:], color='black', linewidth=0.5)
plt.plot(df['VI'].iloc[5:].rolling(7).mean(), color='red')
plt.show()

## Venting index
def rotate(l, n):
    return l[-n:] + l[:-n]

n = 3  # rotate x axis 3 months
vi_m_m = df["VI"].groupby((df.index.month + n) % 12 ).mean()
vi_m_std = df["VI"].groupby((df.index.month + n ) % 12 ).std()
fig, ax = plt.subplots()
ax.fill_between(vi_m_m.index, vi_m_m - 1 * vi_m_std, vi_m_m + 1 * vi_m_std, alpha=0.2)
ax.fill_between(vi_m_m.index, vi_m_m - 2 * vi_m_std, vi_m_m + 2 * vi_m_std, alpha=0.2)
ax.plot(vi_m_m)
ax.set_ylabel("Venting Index")
# ax.set_xticklabels(["Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May",])
ax.set_xticks(range(0,12), rotate(["Jan", "Feb", "Mar", "Apr", "May","Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], n + 1))
ax.set_ylim(0, 100)
ax.set_title(f"Monthly Venting Index ({df.index.year.min()} - {df.index.year.max()})")
fig.show()

