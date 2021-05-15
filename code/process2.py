import os
import json
import pandas as pd
import numpy as np
from ast import literal_eval


def read_json(file_path: str) -> list or dict:
    if not os.path.exists(file_path):
        return None
    with open(file_path, encoding='utf-8') as f:
        rp_list = json.load(f)
    return rp_list


if __name__ == '__main__':
    c = read_json("../data/distance.json")
    df = pd.read_csv("../data/temp1.csv")
    vendor = []
    coordinates = []
    timestamp = []
    _topd = {}
    cnt = 1
    # print(type(literal_eval(df.iloc[0][2])))

    DISTANCE_THRESHOLD = 20

    for index in range(0, len(c)):
        print(index, end='')
        tmp = []
        cord = []
        if len(c[index]) == 1:  # 当距离仅有一个的时候(i.e. 只有两个点的时候)
            if c[index][0] > DISTANCE_THRESHOLD:  # 如果距离大于20km, 直接跳过
                continue
            else:
                cord = literal_eval(df.iloc[index][2])  # 该出租车的所有坐标
                tmp = literal_eval(df.iloc[index][3])  # 该出租车的所有时间戳
                vendor.append(cnt)  # 出租车编号
                cnt += 1  # 出租车编号加1
                coordinates.append(cord)  # 添加到记录中去
                timestamp.append(tmp)  # 添加到记录中去
                cord = []
                tmp = []
        else:
            i = 0
            last_i = -1  # 注意这个last_i
            while True:
                if i == len(c[index]) - 1:  # 当走到最后一个距离差的时候
                    if c[index][i] > DISTANCE_THRESHOLD:
                        cord = literal_eval(df.iloc[index][2])[last_i + 1:-1]
                        tmp = literal_eval(df.iloc[index][3])[last_i + 1:-1]
                    else:
                        cord = literal_eval(df.iloc[index][2])[last_i + 1:]
                        tmp = literal_eval(df.iloc[index][3])[last_i + 1:]

                    vendor.append(cnt)
                    coordinates.append(cord)
                    timestamp.append(tmp)
                    cnt += 1
                    cord = []
                    tmp = []
                    break
                else:  # 后面还有距离差的时候
                    if c[index][i] <= DISTANCE_THRESHOLD:
                        i += 1
                    else:
                        cord = literal_eval(df.iloc[index][2])[last_i + 1:i + 1]
                        tmp = literal_eval(df.iloc[index][3])[last_i + 1:i + 1]
                        vendor.append(cnt)
                        coordinates.append(cord)
                        timestamp.append(tmp)
                        cnt += 1
                        cord = []
                        tmp = []
                        last_i = i  # 更新last_i
                        i+=1
    pd.DataFrame(data={'vendor': vendor, 'coordinates': coordinates, 'timestamp': timestamp}).to_csv(
        "../data/temp2.csv")
