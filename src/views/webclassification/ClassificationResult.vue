<template>
  <el-card class="feature-card">
    <h3>特征抽取结果 (加权TF-IDF)</h3>

    <!-- 权重分布直方图 -->
    <div class="chart-container">
      <canvas ref="weightChart"></canvas>
    </div>

    <!-- 特征权重表格 -->
    <el-table :data="topFeatures" height="300px">
      <el-table-column prop="term" label="特征词" width="150" />
      <el-table-column label="基础TF-IDF">
        <template #default="{ row }">
          <el-tag :type="row.isTitle ? 'success' : ''">
            {{ row.base_weight.toFixed(4) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="weighted" label="加权后" width="120">
        <template #default="{ row }">
          <el-progress
            :percentage="row.weighted * 100"
            :status="row.weighted > 0.1 ? 'success' : 'warning'"
            :show-text="false"
          />
        </template>
      </el-table-column>
      <el-table-column label="来源">
        <template #default="{ row }">
          <el-tag v-if="row.isTitle" type="success">标题</el-tag>
          <el-tag v-else type="info">正文</el-tag>
        </template>
      </el-table-column>
    </el-table>

    <p class="stats">
      特征总数: {{ totalFeatures }} | 标题加权词: {{ titleTermsCount }}
    </p>
  </el-card>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
// import Chart from 'chart.js/auto'
import { useFeatureStore } from '@/store/featureStore'
import { useClassificationStore } from '@/store/classificationStore' // 新增分类状态库

// 1. 统一状态管理
const featureStore = useFeatureStore()
const classificationStore = useClassificationStore() // 集成分类状态

// 2. 响应式数据声明
const weightChart = ref(null)
const topFeatures = ref([])
const totalFeatures = ref(0)
const titleTermsCount = ref(0)

// 3. 计算属性优化（避免重复访问 store）
const weightedMatrix = computed(() => featureStore.weightedMatrix)
const featureVocab = computed(() => featureStore.featureVocab)
const titleTerms = computed(() => featureStore.titleTerms)
const baseTfidf = computed(() => featureStore.baseTfidf)

// 4. 数据处理逻辑封装
const processFeatures = () => {
  if (!weightedMatrix.value) return

  // 使用Map优化词汇表查找性能
  const vocabMap = new Map(
    Object.entries(featureVocab.value).map(([term, idx]) => [idx, term])
  )

  // 取Top20特征（优化排序算法）
  const sortedIndices = [...weightedMatrix.value.data]
    .map((val, idx) => ({ idx, val }))
    .sort((a, b) => b.val - a.val)
    .slice(0, 20)

  topFeatures.value = sortedIndices.map(({ idx, val }) => {
    const term = vocabMap.get(idx)
    return {
      term,
      base_weight: baseTfidf.value[idx],
      weighted: val,
      isTitle: titleTerms.value.includes(term)
    }
  })

  totalFeatures.value = vocabMap.size
  titleTermsCount.value = titleTerms.value.length
}

// 5. 图表生命周期管理
let chartInstance = null

// const initChart = () => {
//   if (chartInstance) chartInstance.destroy() // 销毁旧实例避免内存泄漏
//
//   const ctx = weightChart.value.getContext('2d')
//   chartInstance = new Chart(ctx, {
//     type: 'bar',
//     data: {
//       labels: topFeatures.value.map((f) => f.term),
//       datasets: [
//         {
//           label: '特征权重分布',
//           data: topFeatures.value.map((f) => f.weighted),
//           backgroundColor: topFeatures.value.map((f) =>
//             f.isTitle ? 'rgba(75, 192, 192, 0.8)' : 'rgba(153, 102, 255, 0.6)'
//           ),
//           borderWidth: 1
//         }
//       ]
//     },
//     options: {
//       responsive: true,
//       plugins: {
//         legend: { display: false },
//         tooltip: {
//           callbacks: {
//             label: (ctx) => `权重: ${ctx.raw.toFixed(4)}`
//           }
//         }
//       }
//     }
//   })
// }

// 6. 监听与执行优化
watch(
  weightedMatrix,
  () => {
    processFeatures()
    // initChart()
  },
  { immediate: true }
)

// 7. 组件卸载时清理资源
// onMounted(() => {
//   window.addEventListener('resize', initChart) // 响应窗口缩放
// })
//
// onUnmounted(() => {
//   if (chartInstance) chartInstance.destroy()
//   window.removeEventListener('resize', initChart)
// })
</script>

<style scoped>
.chart-container {
  height: 250px;
  margin-bottom: 20px;
}
.stats {
  margin-top: 15px;
  color: #666;
  font-size: 0.9em;
}
</style>
