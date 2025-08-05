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
import { ref, onMounted, watch } from 'vue'
// import Chart from 'chart.js/auto'
import { useFeatureStore } from '@/store/featureStore'

const props = defineProps(['data'])
const weightChart = ref(null)
const topFeatures = ref([])
const totalFeatures = ref(0)
const titleTermsCount = ref(0)

// 从Pinia状态获取特征数据
const store = useFeatureStore()

// const initChart = () => {
//   const ctx = weightChart.value.getContext('2d')
//   new Chart(ctx, {
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

// 处理特征数据
const processFeatures = () => {
  const features = store.weightedMatrix
  const vocab = store.featureVocab
  const titleTerms = store.titleTerms

  // 取权重最高的20个特征
  const sortedIndices = [...features.data]
    .map((val, idx) => [idx, val])
    .sort((a, b) => b[1] - a[1])
    .slice(0, 20)

  topFeatures.value = sortedIndices.map(([idx, val]) => ({
    term: Object.keys(vocab).find((k) => vocab[k] === idx),
    base_weight: store.baseTfidf[idx],
    weighted: val,
    isTitle: titleTerms.includes(
      Object.keys(vocab).find((k) => vocab[k] === idx)
    )
  }))

  totalFeatures.value = Object.keys(vocab).length
  titleTermsCount.value = titleTerms.length
}

// 监听数据变化
watch(
  () => store.weightedMatrix,
  () => {
    processFeatures()
    // initChart()
  },
  { immediate: true }
)
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
