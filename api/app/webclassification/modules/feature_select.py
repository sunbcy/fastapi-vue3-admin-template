#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/5 上午1:16
# @Author  : sunbcy
# @File    : feature_select.py
# @Software: PyCharm
import numpy as np
from scipy.sparse import csr_matrix


def feature_selection(matrix: csr_matrix, vocab: dict, min_df=0.01, max_df=0.8) -> list[str]:
    """基于文档频率的特征筛选"""
    df = np.diff(matrix.indptr)
    total_docs = matrix.shape[0]
    doc_freq = df / total_docs

    selected_features = [
        term for term, idx in vocab.items()
        if min_df <= doc_freq[idx] <= max_df
    ]
    return selected_features


def run(url):
    return
