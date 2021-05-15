import os
import json
import pandas as pd
import numpy as np
from ast import literal_eval
import random

if __name__ == '__main__':
    df = pd.read_csv("../data/temp2.csv")
    vendor = []
    coordinates = []
    timestamp = []
    color = []
    _topd = {}
    cnt = 1
    for index in range(0, len(df)):
        if len(literal_eval(df.iloc[index][3])) == 1:
            continue
        else:
            vendor.append(cnt)
            cnt += 1
            coordinates.append(literal_eval(df.iloc[index][2]))
            timestamp.append(literal_eval(df.iloc[index][3]))
            color.append([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])

    pd.DataFrame(data={'vendor': vendor, 'coordinates': coordinates, 'timestamp': timestamp, 'color': color}).to_json(
        '../data/temp3.json', orient='records', lines=True)
