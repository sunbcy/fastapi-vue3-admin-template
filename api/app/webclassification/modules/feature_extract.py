#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/5 上午1:16
# @Author  : sunbcy
# @File    : feature_extract.py
# @Software: PyCharm
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix


def feature_weighting(docs: list[list[str]]) -> tuple[csr_matrix, dict]:
    """TF-IDF加权 + 位置权重增强"""
    # 将词列表转换为空格分隔的字符串
    doc_texts = [' '.join(doc) for doc in docs]

    # TF-IDF基础权重
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(doc_texts)

    # 位置权重增强（标题词权重加倍）
    feature_names = vectorizer.get_feature_names_out()
    pos_weights = np.ones(len(feature_names))
    title_terms = set()
    for i, term in enumerate(feature_names):
        if term in title_terms:  # title_terms从HTML解析中提取
            pos_weights[i] = 2.0  # 标题词权重乘2

    weighted_matrix = tfidf_matrix.multiply(pos_weights)
    return weighted_matrix, vectorizer.vocabulary_


def build_tfidf(docs):
    vectorizer = TfidfVectorizer(tokenizer=lambda x: x, preprocessor=lambda x: x, lowercase=False)
    return vectorizer.fit_transform(docs), vectorizer.get_feature_names_out()
