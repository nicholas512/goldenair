import pandas as pd
from pathlib import Path


def read_purpleair(f):
    df = pd.read_csv(f, index_col=0, parse_dates=True, 
                         usecols=['time_stamp',
                                  'pm2.5_alt',
                                  'pm2.5_atm',
                                  'pm2.5_cf_1'])
    return df


def concatenate_directory(dir):
    output_file = Path(dir,"purpleair.csv")
    files = Path(dir).glob("*.csv")
    dfs = []
    for f in files:
        if f == output_file:
            print(f"skipping {f.name}")
            continue
        print(f)
        df = read_purpleair(f)
        station = f.stem.split("_")[0]  # by convention, station is first part of filename
        df.insert(1, column='station', value=station)
        dfs.append(df)
    df = pd.concat(dfs)
    df.to_csv(output_file)


def main(dir):
    concatenate_directory(dir)


if __name__ == "__main__":
    import sys
    dir = sys.argv[1]
    main(dir)