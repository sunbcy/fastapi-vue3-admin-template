#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/5 上午1:16
# @Author  : sunbcy
# @File    : classify.py
# @Software: PyCharm
import joblib
import numpy as np
from scipy.sparse import issparse
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


class DFSelector(TransformerMixin, BaseEstimator):
    def __init__(self, min_df=0.01, max_df=0.8):
        self.min_df = min_df  # 最小文档频率阈值
        self.max_df = max_df  # 最大文档频率阈值

    def fit(self, X, y=None):
        if issparse(X):
            df = np.diff(X.indptr) / X.shape[0]  # 计算文档频率
        else:
            df = (X > 0).sum(axis=0) / X.shape[0]
        self.selected_idx_ = np.where((df >= self.min_df) & (df <= self.max_df))[0]
        return self

    def transform(self, X):
        return X[:, self.selected_idx_]  # 仅保留选定特征


# 构建分类流水线
clf = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('selector', DFSelector(min_df=0.01, max_df=0.8)),  # 自定义特征选择器
    ('nb', MultinomialNB(alpha=0.1))
])


# 分布式训练支持
def train_model(docs, labels):
    clf.fit(docs, labels)
    # 模型持久化
    joblib.dump(clf, "nb_classifier.joblib")
