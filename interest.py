#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from ItemRank import ItemRank
from mean import Mean

if __name__ == "__main__":
    # 从文件中读取数据
    pd_data = pd.read_csv("D:/ml-latest-small/ratings_test.csv")
    np_data = pd_data.values
    item_rank = ItemRank(np_data)
    print("***生成图模型中***")
    item_rank.generate_graph()
    print("***计算相关系数中***")
    item_rank.generate_coef_from_graph()
    print("***生成评分向量中***")
    d = item_rank.generate_d(user_name=2)
    IR = d
    print("***计算itemrank中***")
    covered = False
    counter = 0
    while not covered:
        counter += 1
        old_IR = IR
        IR = item_rank.item_rank(0.85, IR, d)
        covered = (old_IR - IR < 0.0001).all()
    print("IR now is ", IR)
    # 得到电影的itemrank值
    # print(IR[item_rank.movie_names.index(2)])
    mean = Mean(pd_data)
    average = mean.calc_mean(2)
    movie_by_time = average.index.tolist()
    IR_by_time = []
    for m in movie_by_time:
        IR_by_time.append(IR[item_rank.movie_names.index(m)])
    IR_by_time = {'IR': IR_by_time}
    IR_by_time = pd.DataFrame(IR_by_time).set_index(pd.Series(movie_by_time))
    result = average.merge(IR_by_time, left_index=True, right_index=True, how="outer")
    print(result)
