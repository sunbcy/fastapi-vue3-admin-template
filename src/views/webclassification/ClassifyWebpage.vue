<template>
  <div class="container">
    <!-- 输入区域 -->
    <el-card class="input-card">
      <el-input v-model="url" placeholder="输入网页URL" clearable>
        <template #append>
          <el-button type="primary" @click="startProcessing" :loading="loading"
            >开始分类</el-button
          >
        </template>
      </el-input>
    </el-card>

    <!-- 流程展示 -->
    <el-steps :active="activeStep" finish-status="success" align-center>
      <el-step title="网页预处理" description="HTML解析/分词/清洗" />
      <el-step title="特征抽取" description="TF-IDF加权/位置增强" />
      <el-step title="特征选择" description="文档频率筛选" />
      <el-step title="分类预测" description="朴素贝叶斯分类" />
    </el-steps>

    <!-- 结果展示 -->
    <component :is="currentComponent" :data="stepData" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import PreprocessResults from './PreprocessResults.vue'
import FeatureExtraction from './FeatureExtraction.vue'
import FeatureSelection from './FeatureSelection.vue'
import ClassificationResult from './ClassificationResult.vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const url = ref('https://www.baidu.com')
const loading = ref(false)
const activeStep = ref(0)
const stepData = ref({})

const components = [
  PreprocessResults,
  FeatureExtraction,
  FeatureSelection,
  ClassificationResult
]

const currentComponent = computed(() => components[activeStep.value])

const startProcessing = async () => {
  loading.value = true
  try {
    const response = await axios.post('/api/webclassification/process', {
      url: url.value
    })
    stepData.value = response.data

    // 模拟流程进度
    const steps = Object.keys(response.data)
    for (let i = 0; i < steps.length; i++) {
      activeStep.value = i
      await new Promise((resolve) => setTimeout(resolve, 800))
    }
  } catch (error) {
    ElMessage.error('处理失败: ' + error.message)
  } finally {
    loading.value = false
  }
}
</script>
