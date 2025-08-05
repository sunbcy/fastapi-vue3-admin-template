<template>
  <el-card class="selection-card">
    <h3>特征选择 (文档频率筛选)</h3>

    <!-- 维度变化对比 -->
    <div class="dim-comparison">
      <div class="dim-box original">
        <h4>原始维度</h4>
        <el-statistic :value="originalDim" />
      </div>
      <el-icon :size="40"><ArrowRight /></el-icon>
      <div class="dim-box selected">
        <h4>筛选后维度</h4>
        <el-statistic :value="selectedDim" />
        <el-tag type="success" effect="dark">
          压缩率: {{ compressionRate }}%
        </el-tag>
      </div>
    </div>

    <!-- DF分布直方图 -->
    <div class="chart-container">
      <canvas ref="dfChart"></canvas>
    </div>

    <!-- 筛选参数说明 -->
    <el-descriptions title="筛选参数" :column="2" border>
      <el-descriptions-item label="最小DF">
        <el-tag size="small">0.01</el-tag> (出现率≥1%)
      </el-descriptions-item>
      <el-descriptions-item label="最大DF">
        <el-tag size="small">0.8</el-tag> (出现率≤80%)
      </el-descriptions-item>
    </el-descriptions>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
// import Chart from 'chart.js/auto'
import { ArrowRight } from '@element-plus/icons-vue'
import { useFeatureStore } from '@/store/featureStore'

const dfChart = ref(null)
const store = useFeatureStore()

const originalDim = computed(() => store.featureSelection?.originalDim || 0)
const selectedDim = computed(() => store.featureSelection?.selectedDim || 0)
const compressionRate = computed(() =>
  Math.round((1 - selectedDim.value / originalDim.value) * 100)
)

// const initChart = () => {
//   if (!store.featureSelection) return
//
//   const ctx = dfChart.value.getContext('2d')
//   const dfData = store.featureSelection.dfDistribution
//
//   // 生成DF分布直方图
//   new Chart(ctx, {
//     type: 'bar',
//     data: {
//       labels: dfData.map(
//         (_, i) => `${Math.round(i * 10)}%-${Math.round((i + 1) * 10)}%`
//       ),
//       datasets: [
//         {
//           label: '特征分布',
//           data: dfData,
//           backgroundColor: 'rgba(54, 162, 235, 0.6)',
//           borderColor: 'rgba(54, 162, 235, 1)',
//           borderWidth: 1
//         }
//       ]
//     },
//     options: {
//       responsive: true,
//       plugins: {
//         annotation: {
//           annotations: {
//             minLine: {
//               type: 'line',
//               yMin: 0.01,
//               yMax: 0.01,
//               borderColor: 'red',
//               borderWidth: 2,
//               label: {
//                 display: true,
//                 content: '最小DF阈值',
//                 position: 'end'
//               }
//             },
//             maxLine: {
//               type: 'line',
//               yMin: 0.8,
//               yMax: 0.8,
//               borderColor: 'orange',
//               borderWidth: 2,
//               label: {
//                 display: true,
//                 content: '最大DF阈值',
//                 position: 'end'
//               }
//             }
//           }
//         }
//       },
//       scales: {
//         y: {
//           title: { text: '文档频率', display: true },
//           min: 0,
//           max: 1
//         },
//         x: { title: { text: '频率区间', display: true } }
//       }
//     }
//   })
// }

// 监听数据更新
watch(() => store.featureSelection, { immediate: true }) // , initChart
</script>

<style scoped>
.dim-comparison {
  display: flex;
  align-items: center;
  justify-content: space-around;
  margin: 20px 0;
}
.dim-box {
  text-align: center;
  padding: 15px;
  border-radius: 8px;
  width: 45%;
}
.original {
  background: #f0f9ff;
  border: 1px dashed #409eff;
}
.selected {
  background: #f0f9e8;
  border: 1px dashed #67c23a;
}
</style>
