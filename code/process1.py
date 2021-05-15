# %%

import pandas as pd
import numpy as np
from geopy.distance import geodesic
import pycuda
import os
import json


def write_json(file_path: str, file_name: str, info: list or dict):
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    json_str = json.dumps(info, indent=4)
    with open("{0}/{1}".format(file_path, file_name), 'w', encoding='utf-8') as f:
        f.write(json_str)
    f.close()


if __name__ == '__main__':
    # %%
    data = pd.read_csv("../data/sample_taxi.csv")
    # %%
    data = data[data['lat'] <= 22.866666667]
    data = data[22.366666667 <= data['lat']]
    data = data[data['lon'] <= 114.583333333]
    data = data[113.75 <= data['lon']]
    # %%
    data.columns = ['vendor', 'time', 'lon', 'lat', 'has_passenger', 'speed']
    data['coordinates'] = data.apply(lambda r: [r['lon'], r['lat']], axis=1)
    data['timestamp'] = data['time'].str.slice(0, 2).astype('int') * 3600 + data['time'].str.slice(3, 5).astype(
        'int') * 60 + data['time'].str.slice(6, 8).astype('int') * 1
    data = data.sort_values(by=['vendor', 'timestamp'])
    data['coordinates'] = data['coordinates'].apply(lambda r: [r])
    data['timestamp'] = data['timestamp'].apply(lambda r: [r])
    df = data.groupby('vendor')['coordinates', 'timestamp'].sum()
    df = df.reset_index()
    # %%
    df['len'] = df['coordinates'].str.len()
    # %%
    df = df[df['len'] > 1]
    df.to_csv("../data/temp1.csv")

    b = list(df['coordinates'])
    # %%
    c = []
    for entry in b:
        d = []
        for i in range(0, len(entry) - 1):
            d.append(geodesic((entry[i][1], entry[i][0]), (entry[i + 1][1], entry[i + 1][0])).km)
        c.append(d)
    write_json("../data", "distance.json", c)
