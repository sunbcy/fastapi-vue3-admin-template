#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/5 上午1:16
# @Author  : sunbcy
# @File    : feature_extract.py
# @Software: PyCharm
from pathlib import Path

import joblib
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

# 预训练向量化器路径（需提前训练保存）
VECTORIZER_PATH = Path(__file__).parent / "tfidf_vectorizer.pkl"


# def feature_weighting(docs: list[list[str]]) -> tuple[csr_matrix, dict]:
#     """TF-IDF加权 + 位置权重增强"""
#     # 将词列表转换为空格分隔的字符串
#     doc_texts = [' '.join(doc) for doc in docs]
#
#     # TF-IDF基础权重
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(doc_texts)
#
#     # 位置权重增强（标题词权重加倍）
#     feature_names = vectorizer.get_feature_names_out()
#     pos_weights = np.ones(len(feature_names))
#     title_terms = set()
#     for i, term in enumerate(feature_names):
#         if term in title_terms:  # title_terms从HTML解析中提取
#             pos_weights[i] = 2.0  # 标题词权重乘2
#
#     weighted_matrix = tfidf_matrix.multiply(pos_weights)
#     return weighted_matrix, vectorizer.vocabulary_
#
#
# def build_tfidf(docs):
#     vectorizer = TfidfVectorizer(tokenizer=lambda x: x, preprocessor=lambda x: x, lowercase=False)
#     return vectorizer.fit_transform(docs), vectorizer.get_feature_names_out()
#
#
# def run(url):
#     return

def feature_weighting(
        docs: list[list[str]],
        title_terms: set = None
) -> tuple[csr_matrix, dict]:
    """
    TF-IDF加权 + 位置权重增强
    :param docs: 分词后的文档列表，每个元素是词列表
    :param title_terms: 标题词集合（从HTML标题提取的关键词）
    :return: 加权特征矩阵, 词汇表
    """
    # 转换为空格分隔的文本
    doc_texts = [' '.join(doc) for doc in docs]

    # 加载预训练向量化器（避免单文档IDF失效）
    vectorizer = _load_vectorizer()
    tfidf_matrix = vectorizer.transform(doc_texts)
    vocab = vectorizer.vocabulary_

    # 位置权重增强（标题词权重加倍）
    feature_names = vectorizer.get_feature_names_out()
    pos_weights = np.ones(len(feature_names))

    if title_terms:
        for i, term in enumerate(feature_names):
            if term in title_terms:
                pos_weights[i] = 2.0  # 标题词权重加倍

    # 应用位置权重
    weighted_matrix = tfidf_matrix.multiply(pos_weights)
    return weighted_matrix, vocab


def _load_vectorizer() -> TfidfVectorizer:
    """加载预训练的TF-IDF向量化器"""
    if VECTORIZER_PATH.exists():
        return joblib.load(VECTORIZER_PATH)
    else:
        raise FileNotFoundError(
            "预训练向量化器未找到，请先执行训练流程生成tfidf_vectorizer.pkl"
        )


def run(tokens: list[str], title_tokens: list[str] = None) -> csr_matrix:
    """
    特征抽取主函数
    :param tokens: 分词结果列表，如['关于','百度','使用',...]
    :param title_tokens: 标题分词列表（可选）
    :return: 加权特征矩阵（CSR稀疏格式）
    """
    # 将标题分词转换为集合（如提供）
    title_terms = set(title_tokens) if title_tokens else None

    # 执行特征加权（单文档需包装为列表）
    matrix, _ = feature_weighting([tokens], title_terms)
    return matrix


# ---------------------- 训练时使用的函数（非线上服务调用）----------------------
def train_vectorizer(corpus: list[list[str]], save_path: Path = VECTORIZER_PATH):
    """
    训练并保存TF-IDF向量化器（需在数据准备阶段执行）
    :param corpus: 训练语料，每个元素是分词后的词列表
    :param save_path: 模型保存路径
    """
    # 转换为文本
    corpus_texts = [' '.join(doc) for doc in corpus]

    # 训练向量化器（保留原始分词结果）
    vectorizer = TfidfVectorizer(
        tokenizer=lambda x: x,
        preprocessor=lambda x: x,
        lowercase=False,
        min_df=0.01,  # 过滤低频词
        max_df=0.8,  # 过滤高频词
        use_idf=True,
        smooth_idf=True
    )
    vectorizer.fit(corpus_texts)
    joblib.dump(vectorizer, save_path)
    return vectorizer
