#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/5 上午1:16
# @Author  : sunbcy
# @File    : preprocess.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup
import jieba
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


# 初始化资源
nltk.download('punkt')
nltk.download('stopwords')
jieba.initialize()


def html_parser(html: str) -> str:
    """HTML解析：提取纯文本并保留语义结构"""
    soup = BeautifulSoup(html, 'lxml')
    # 移除脚本/样式
    for tag in soup(["script", "style", "header", "footer"]):
        tag.decompose()
    # 提取主体文本并保留段落分隔
    text = '\n'.join(p.get_text().strip() for p in soup.find_all(['p', 'h1', 'h2', 'h3']))
    return text


def tokenize_mixed_text(text: str) -> list:
    """中英文混合分词"""
    # 英文词法分析
    eng_tokens = word_tokenize(re.sub(r'[^\w\s]', '', text))
    # 中文分词（精确模式）
    chn_text = ''.join(eng_tokens)
    chn_tokens = jieba.lcut(chn_text, cut_all=False)
    return eng_tokens + chn_tokens


def preprocess_pipeline(html: str) -> list[str]:
    """预处理流水线"""
    text = html_parser(html)
    tokens = tokenize_mixed_text(text)
    # 停用词过滤（中英文）
    stops = set(stopwords.words('english')) | set(open('cn_stopwords.txt').read().splitlines())
    filtered = [word for word in tokens if word.lower() not in stops and len(word) > 1]
    # 英文词干提取
    stemmer = PorterStemmer()
    stemmed = [stemmer.stem(word) if word.isascii() else word for word in filtered]
    return stemmed


# def run(url):
#     # 1. 获取网页内容
#     response = requests.get(url)
#     html = response.text
#
#     # 2. HTML解析
#     soup = BeautifulSoup(html, 'lxml')
#     for tag in soup(["script", "style", "header", "footer"]):
#         tag.decompose()
#     clean_text = '\n'.join(p.get_text().strip() for p in soup.find_all(['p', 'h1', 'h2', 'h3']))
#
#     # 3. 中英文分词
#     chinese_text = re.sub(r'[^\u4e00-\u9fa5]', ' ', clean_text)
#     english_text = re.sub(r'[^a-zA-Z]', ' ', clean_text)
#     chn_tokens = jieba.lcut(chinese_text)
#     eng_tokens = word_tokenize(english_text)
#
#     # 4. 停用词过滤
#     stops = set(stopwords.words('english')) | set(open('cn_stopwords.txt').read().splitlines())
#     filtered = [word for word in chn_tokens + eng_tokens
#                 if word.lower() not in stops and len(word) > 1]
#
#     # 5. 词干提取
#     stemmer = PorterStemmer()
#     stemmed = [stemmer.stem(word) if word.isascii() else word for word in filtered]
#
#     return {
#         "original_html": html[:500] + "...",
#         "clean_text": clean_text,
#         "tokens": stemmed
#     }

def parse_html(html: str):
    soup = BeautifulSoup(html, 'lxml')
    text_parts = [
        soup.title.string if soup.title else '',
        ' '.join([h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])]),
        ' '.join([p.get_text() for p in soup.find_all('p')])
    ]
    return '\n'.join(text_parts)


def tokenize_en(text: str):
    return word_tokenize(text)


def tokenize_zh(text: str):
    return list(jieba.cut(text))


def remove_stopwords(tokens, stopwords):
    return [word for word in tokens if word.lower() not in stopwords]


# 加载中英文停用词
with open("stopwords.txt", encoding='utf-8') as f:
    stopwords = set(f.read().splitlines())


def stem_en(tokens):
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in tokens]

def select_terms(tokens):
    return [t for t in tokens if len(t) > 1]

def preprocess_pipeline(html):
    text = parse_html(html)
    tokens_en = tokenize_en(text)
    tokens_en = stem_en(tokens_en)
    tokens_zh = tokenize_zh(text)
    tokens = tokens_en + tokens_zh
    tokens = remove_stopwords(tokens, stopwords)
    return select_terms(tokens)


