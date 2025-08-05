# ---
# -*- coding: utf-8 -*-
# @Software: PyCharm
# @File: routes.py
# @Author: sunbcy
# @Institution: SYLG University, ShenZhen, China
# @E-mail: saintbcy@163.com
# @Time: 11月 02, 2024 21:56
# ---
from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel

from app.webclassification.modules import preprocess, feature_extract, feature_select, classify

router = APIRouter()


class ProcessRequest(BaseModel):
    url: str


@router.post("/process")
async def full_pipeline(request: ProcessRequest):
    try:
        # 1. 网页预处理
        preprocess_result = preprocess.run(request.url)

        # 2. 特征抽取
        features = feature_extract.run(preprocess_result['tokens'])

        # 3. 特征选择
        selected_features = feature_select.run(features)

        # 4. 分类预测
        classification = classify.run(selected_features)

        return {
            "preprocess": preprocess_result,
            "feature_extraction": features.to_dict(),
            "feature_selection": selected_features,
            "classification": classification
        }
    except Exception as e:
        raise HTTPException(500, f"处理失败: {str(e)}")
