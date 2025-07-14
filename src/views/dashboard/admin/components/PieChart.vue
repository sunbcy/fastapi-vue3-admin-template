<script setup>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from '@/views/dashboard/admin/components/mixins/resi'
import { get_top_ten_industries } from '@/api/liepin'
import { nextTick, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'

const mixins = ref([resize])
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
  }
})
const chart = ref(null)

// 定义initChart方法
const initChart = async () => {
  // 初始化图表的逻辑
  chart.value = echarts.init(this.$el, 'macarons')

  try {
    const res = await get_top_ten_industries()
    chart.value.setOption({
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
      },
      legend: {
        left: 'center',
        bottom: '10',
        data: res.searchResults.map((item) => item.name)
        // ['互联网', '计算机软件', '电子商务', '电子/半导体/集成电路', '通信设备', 'IT服务', '批发/零售', '贸易/进出口', '专业技术服务', '机械/设备']
      },
      series: [
        {
          name: '猎聘行业职位数目',
          type: 'pie',
          roseType: 'radius',
          radius: [15, 95],
          center: ['50%', '38%'],
          animationEasing: 'cubicInOut',
          animationDuration: 2600,
          data: res.searchResults
        }
      ]
    })
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常，获取失败')
  }
}

onMounted(() => {
  nextTick(() => {
    initChart()
  })
})
</script>

<template>
  <div :class="className" :style="{ height: height, width: width }" />
</template>

<style scoped lang="scss"></style>
