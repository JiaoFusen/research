#!/user/bin/python
# -*- coding: utf-8 -*-
# 以平均分为评价指标来测度用户兴趣的演化
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Mean(object):
    def __init__(self, pd_data):
        self.rating = pd_data
        self.user_movie = []

    #   计算平均分
    def calc_mean(self, user):
        movie_rating = self.rating.loc[:, ['movieId', 'rating']]
        average_rating = movie_rating.groupby('movieId').mean()
        user_rating = self.rating[self.rating.userId == user].sort_index(by='timestamp')
        self.user_movie = user_rating.movieId.tolist()  # 用户看过的电影集合
        user_rating = user_rating.loc[:, ['movieId', 'rating', 'timestamp']]
        user_aver_rating = average_rating.loc[self.user_movie]
        user_rating = user_rating.merge(user_aver_rating, right_index=True, how="outer", left_on='movieId')
        user_rating1 = user_rating.loc[:, ['rating_x', 'rating_y']]
        # user_rating1.reindex(np.arange(len(user_rating1)))
        index = np.arange(len(user_rating1))
        user_rating1.set_index(index)
        print(user_rating1)


if __name__ == "__main__":
    pd_data = pd.read_csv("/Users/JiaoFusen/Desktop/ml-latest-small/ratings.csv")
    mean = Mean(pd_data)
    mean.calc_mean(288)
