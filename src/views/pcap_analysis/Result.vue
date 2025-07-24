<template>
  <div class="result-container">
    <div class="chart-wrapper">
      <PieChart v-if="fetchedInfo" :fetched-info="fetchedInfo" />
    </div>

    <div class="info-container">
      <h2 class="section-title">分析结果详情</h2>
      <el-alert
        v-if="!fetchedInfo"
        title="正在加载分析结果..."
        type="info"
        show-icon
        class="loading-alert"
      />

      <div v-if="fetchedInfo" class="result-content">
        <el-row :gutter="20" class="info-row">
          <el-col :span="12">
            <el-card shadow="hover" class="info-card">
              <template v-slot:header>
                <div class="card-header">
                  <i class="el-icon-s-data"></i>
                  <span>基本信息</span>
                </div>
              </template>
              <div class="card-content">
                <p>
                  <strong>数据包名称:</strong>
                  {{ fetchedInfo.packet_name || '未知' }}
                </p>
                <p><strong>分析时间:</strong> {{ formattedTime }}</p>
                <p><strong>文件大小:</strong> {{ fileSize }}</p>
              </div>
            </el-card>
          </el-col>

          <el-col :span="12">
            <el-card shadow="hover" class="info-card">
              <template v-slot:header>
                <div class="card-header">
                  <i class="el-icon-cpu"></i>
                  <span>统计概览</span>
                </div>
              </template>
              <div class="card-content">
                <p><strong>协议种类:</strong> {{ protocolCount }} 种</p>
                <p>
                  <strong>数据包总数:</strong>
                  {{ fetchedInfo.protocol_info?.total_packets || 0 }} 个
                </p>
                <p><strong>持续时间:</strong> {{ duration }}</p>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-card shadow="hover" class="protocol-card">
          <template v-slot:header>
            <div class="card-header">
              <i class="el-icon-connection"></i>
              <span>协议分布明细</span>
            </div>
          </template>
          <div class="card-content">
            <el-table :data="protocolDetails" height="300" style="width: 100%">
              <el-table-column prop="protocol" label="协议名称" width="180" />
              <el-table-column prop="count" label="数量">
                <template #default="{ row }">
                  {{ row.count }} ({{ row.percentage }}%)
                </template>
              </el-table-column>
              <el-table-column label="比例">
                <template #default="{ row }">
                  <el-progress
                    :percentage="row.percentage"
                    :color="row.color"
                  ></el-progress>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ElLoading, ElMessage } from 'element-plus'
import PieChart from './PieChart.vue'

// 定义组件 Props
const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  },
  tableData: {
    type: Array,
    required: true
  }
})

// 响应式数据
const fetchedInfo = ref(null)
const loading = ref(false)

// 计算属性
const formattedTime = computed(() => {
  if (!fetchedInfo.value?.analysis_time) return '未知'
  const date = new Date(fetchedInfo.value.analysis_time)
  return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`
})

const fileSize = computed(() => {
  if (!fetchedInfo.value?.file_size) return '未知'
  const sizeInKb = fetchedInfo.value.file_size / 1024
  return sizeInKb > 1024
    ? `${(sizeInKb / 1024).toFixed(2)} MB`
    : `${sizeInKb.toFixed(2)} KB`
})

const duration = computed(() => {
  if (!fetchedInfo.value?.protocol_info?.duration_seconds) return '未知'
  const seconds = fetchedInfo.value.protocol_info.duration_seconds
  if (seconds < 60) return `${seconds} 秒`
  return `${Math.floor(seconds / 60)} 分 ${Math.floor(seconds % 60)} 秒`
})

const protocolCount = computed(() => {
  if (!fetchedInfo.value?.protocol_info?.protocol_types) return 0
  return Object.keys(fetchedInfo.value.protocol_info.protocol_types).length
})

const protocolDetails = computed(() => {
  if (!fetchedInfo.value?.protocol_info?.protocol_types) return []

  const total = fetchedInfo.value.protocol_info.total_packets || 1
  const colors = [
    '#5470c6',
    '#91cc75',
    '#fac858',
    '#ee6666',
    '#73c0de',
    '#3ba272',
    '#fc8452',
    '#9a60b4'
  ]

  return Object.entries(fetchedInfo.value.protocol_info.protocol_types)
    .map(([protocol, count], index) => {
      const percentage = Math.round((count / total) * 100)
      return {
        protocol,
        count,
        percentage,
        color: colors[index % colors.length]
      }
    })
    .sort((a, b) => b.count - a.count)
})

// 方法
const fetchResult = () => {
  // 显示加载状态
  loading.value = true
  const loadingInstance = ElLoading.service({
    target: '.result-container',
    text: '正在加载分析结果...'
  })

  try {
    // 根据提供的ID在tableData中查找匹配项
    const result = props.tableData.find((item) => item.id === Number(props.id))

    if (result) {
      fetchedInfo.value = result.ret_info
      ElMessage.success('分析结果加载成功!')
    } else {
      ElMessage.error(`找不到ID为 ${props.id} 的分析结果`)
    }
  } catch (error) {
    console.error('加载结果失败:', error)
    ElMessage.error(`加载分析结果失败: ${error.message || '未知错误'}`)
  } finally {
    loadingInstance.close()
    loading.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  fetchResult()
})

// 监听props变化
watch(
  () => props.id,
  (newId) => {
    console.log(`ID变化为 ${newId}, 重新加载数据`)
    fetchResult()
  }
)
</script>

<style scoped>
.result-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.section-title {
  color: #303133;
  margin-bottom: 25px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.chart-wrapper {
  background-color: #fff;
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.info-container {
  background-color: #fff;
  border-radius: 4px;
  padding: 25px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.loading-alert {
  margin: 20px 0;
}

.info-row {
  margin-bottom: 20px;
}

.info-card {
  margin-bottom: 20px;
  border-radius: 8px;
}

.protocol-card {
  border-radius: 8px;
  margin-top: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  font-weight: bold;
  color: #303133;
}

.card-header i {
  margin-right: 8px;
  font-size: 18px;
}

.card-content {
  padding: 10px 0;
  color: #606266;
  line-height: 24px;
}

.card-content p {
  margin: 10px 0;
}
</style>
