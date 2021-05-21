import pandas as pd
from geopy.distance import geodesic
from myUtils import write_json

INPUT_CSV = "../data/sample_taxi.csv"
OUTPUT_CSV = "../data/temp1.csv"

def calculate_diff():
    """
    To calculate the distance between 2 coordinates and write it into files
    :return: None
    """
    b = list(df['coordinates'])
    c = []
    for entry in b:
        d = []
        for i in range(0, len(entry) - 1):
            d.append(geodesic((entry[i][1], entry[i][0]), (entry[i + 1][1], entry[i + 1][0])).km)
        c.append(d)
    write_json("../data", "distance.json", c)


if __name__ == '__main__':
    # read the data
    data = pd.read_csv(INPUT_CSV)

    # exclude the data outside Shenzhen
    data = data[data['lat'] <= 22.866666667]
    data = data[22.366666667 <= data['lat']]
    data = data[data['lon'] <= 114.583333333]
    data = data[113.75 <= data['lon']]

    # aggregate the data by taxi_id
    data.columns = ['vendor', 'time', 'lon', 'lat', 'has_passenger', 'speed']
    data['coordinates'] = data.apply(lambda r: [r['lon'], r['lat']], axis=1)
    data['timestamp'] = data['time'].str.slice(0, 2).astype('int') * 3600 + data['time'].str.slice(3, 5).astype(
        'int') * 60 + data['time'].str.slice(6, 8).astype('int') * 1
    data = data.sort_values(by=['vendor', 'timestamp'])
    data['coordinates'] = data['coordinates'].apply(lambda r: [r])
    data['timestamp'] = data['timestamp'].apply(lambda r: [r])
    df = data.groupby('vendor')['coordinates', 'timestamp'].sum()
    df = df.reset_index()

    # drop the rows that contains only 1 coordinates (1 row)
    df['len'] = df['coordinates'].str.len()
    df = df[df['len'] > 1]

    # export the data
    df.to_csv(OUTPUT_CSV)

    calculate_diff()
