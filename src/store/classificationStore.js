import { defineStore } from 'pinia'

export const useClassificationStore = defineStore('classification', {
  state: () => ({
    prediction: {
      label: '', // 预测类别
      confidence: 0, // 置信度 (0-1)
      classProbabilities: {} // 各类别概率分布 {科技: 0.92, 体育: 0.05, ...}
    },
    metrics: {
      processTime: 0, // 分类处理时间(ms)
      inputDim: 0, // 输入特征维度
      outputDim: 0 // 输出特征维度
    }
  }),
  actions: {
    // 更新分类结果
    updatePrediction(result) {
      this.prediction = {
        label: result.category,
        confidence: result.confidence,
        classProbabilities: result.class_probabilities
      }
    },
    // 更新处理指标
    updateMetrics(metrics) {
      this.metrics = {
        processTime: metrics.process_time,
        inputDim: metrics.input_dim,
        outputDim: metrics.output_dim
      }
    },
    // 重置状态
    $reset() {
      this.prediction = { label: '', confidence: 0, classProbabilities: {} }
      this.metrics = { processTime: 0, inputDim: 0, outputDim: 0 }
    }
  }
})
