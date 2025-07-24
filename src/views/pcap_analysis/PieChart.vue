<template>
  <div ref="chartRef" :class="className" :style="{ height, width }" />
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch, defineProps } from 'vue'
import * as echarts from 'echarts'
import 'echarts/theme/macarons' // echarts theme

const props = defineProps({
  className: {
    type: String,
    default: 'chart'
  },
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '300px'
  },
  fetchedInfo: {
    type: Object,
    required: true
  }
})

const chartRef = ref(null)
let chartInstance = null

// 监听窗口大小变化（替代 resize mixin）
const handleResize = () => {
  chartInstance && chartInstance.resize()
}

const initChart = () => {
  if (!chartRef.value) return

  // 销毁现有图表实例
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }

  // 创建新的图表实例
  chartInstance = echarts.init(chartRef.value, 'macarons')

  // 确保 fetchedInfo 数据存在
  if (props.fetchedInfo && props.fetchedInfo.protocol_info) {
    const legendData = Object.keys(
      props.fetchedInfo.protocol_info.protocol_types
    )

    const seriesData = Object.entries(
      props.fetchedInfo.protocol_info.protocol_types
    ).map(([name, value]) => ({
      value,
      name
    }))

    chartInstance.setOption({
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
      },
      legend: {
        left: 'center',
        bottom: '10',
        data: legendData,
        type: 'scroll' // 处理长图例滚动
      },
      series: [
        {
          name: 'Pcap Protocol Analysis',
          type: 'pie',
          roseType: 'radius',
          radius: [15, 95],
          center: ['50%', '38%'],
          data: seriesData,
          animationEasing: 'cubicInOut',
          animationDuration: 2600,
          // 数据过多时的标签优化
          label: {
            formatter: '{b}: {d}%',
            overflow: 'truncate',
            width: 80
          }
        }
      ]
    })
  }

  // 添加窗口调整大小事件监听器
  window.addEventListener('resize', handleResize)
}

// 监听传入数据的变化
watch(
  () => props.fetchedInfo,
  (newVal) => {
    if (newVal) {
      initChart()
    }
  },
  { deep: true }
)

// 生命周期钩子
onMounted(() => {
  initChart()
})

onBeforeUnmount(() => {
  // 销毁图表实例
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }

  // 移除事件监听器
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.chart {
  transition: all 0.3s;
}
</style>
