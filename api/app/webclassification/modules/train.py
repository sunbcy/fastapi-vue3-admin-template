#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/9 上午4:26
# @Author  : sunbcy
# @File    : train.py
# @Software: PyCharm
# 数据准备脚本（train.py）
from feature_extract import train_vectorizer

# 加载训练语料（示例）
corpus = [
    ["人工", "智能", "应用", "系统", "设计"],
    ["深度", "学习", "驱动", "医疗", "影像"],
    # ... 百万级文档
]

# 训练并保存向量化器
vectorizer = train_vectorizer(corpus)
print(f"词汇表大小: {len(vectorizer.vocabulary_)}")
