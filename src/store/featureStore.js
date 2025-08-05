import { defineStore } from 'pinia'

export const useFeatureStore = defineStore('features', {
  state: () => ({
    weightedMatrix: null, // CSR格式特征矩阵
    featureVocab: {}, // 特征词典
    titleTerms: [], // 标题词列表[1](@ref)
    featureSelection: null // 特征选择结果
  })
})
