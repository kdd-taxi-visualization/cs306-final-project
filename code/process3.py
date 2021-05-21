import pandas as pd
from ast import literal_eval
import random

CSV_FILE = "../data/temp2-2km.csv"
OUTPUT_FILE = '../data/temp3-2km.json'

if __name__ == '__main__':
    df = pd.read_csv(CSV_FILE)
    vendor = []
    coordinates = []
    timestamp = []
    color = []
    cnt = 1
    for index in range(0, len(df)):
        if len(literal_eval(df.iloc[index][3])) == 1:
            continue
        else:
            vendor.append(cnt)
            cnt += 1
            coordinates.append(literal_eval(df.iloc[index][2]))
            timestamp.append(literal_eval(df.iloc[index][3]))
            color.append([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])  # 生成随机颜色

    pd.DataFrame(
        data={
            'vendor': vendor,
            'coordinates': coordinates,
            'timestamp': timestamp,
            'color': color}
    ).to_json(OUTPUT_FILE, orient='records', lines=True)
