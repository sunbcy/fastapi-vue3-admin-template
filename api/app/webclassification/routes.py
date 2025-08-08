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
from traceback import print_exc
from pprint import pprint

from app.webclassification.modules import preprocess, feature_extract, feature_select, classify

router = APIRouter()


class ProcessRequest(BaseModel):
    url: str


@router.post("/process")
def full_pipeline(request: ProcessRequest):
    print(request.url)
    try:
        # 1. 网页预处理
        preprocess_result = preprocess.run(request.url)
        pprint(preprocess_result)

    except Exception as e:
        print_exc()
        raise HTTPException(500, f"处理失败: {str(e)}")

    try:
        # 2. 特征抽取
        features = feature_extract.run(preprocess_result['tokens'])
        pprint(features)
    except Exception as e:
        print_exc()
        raise HTTPException(500, f"处理失败: {str(e)}")

    try:
        # 3. 特征选择
        selected_features = feature_select.run(features)
        pprint(selected_features)
    except Exception as e:
        print_exc()
        raise HTTPException(500, f"处理失败: {str(e)}")

    try:
        # 4. 分类预测
        classification = classify.run(selected_features)
    except Exception as e:
        print_exc()
        raise HTTPException(500, f"处理失败: {str(e)}")
    pprint({
        "preprocess": preprocess_result,
        "feature_extraction": features.to_dict(),
        "feature_selection": selected_features,
        "classification": classification
    })

    return {
        "preprocess": preprocess_result,
        "feature_extraction": features.to_dict(),
        "feature_selection": selected_features,
        "classification": classification
    }
    # except Exception as e:
    #     raise HTTPException(500, f"处理失败: {str(e)}")
