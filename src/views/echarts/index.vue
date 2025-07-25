<template>
  <div class="dashboard-container">
    <!-- 左侧菜单栏 -->
    <div class="menu-sidebar">
      <div class="logo">ECharts 示例</div>
      <el-menu
        default-active="line-chart"
        class="menu"
        @select="handleMenuSelect"
      >
        <!-- <div class="subtitle">图表类型</div> -->
        <!-- 使用 v-for 循环确保菜单项结构一致 -->
        <el-menu-item v-for="item in menuItems" :key="item.id" :index="item.id">
          <i :class="item.icon" />
          <span>{{ item.name }}</span>
          <span class="lang-count">
            {{ item.langCount }}<i class="el-icon-document" />
          </span>
        </el-menu-item>
        <div class="divider" />
      </el-menu>
    </div>
    <!-- 右侧内容区 -->
    <div class="content-container">
      <div class="header">
        <div class="search-box">
          <el-input placeholder="搜索示例..." suffix-icon="el-icon-search" />
        </div>
        <div class="actions">
          <el-button>深色模式</el-button>
          <el-button>EN</el-button>
          <el-button type="primary">下载</el-button>
        </div>
      </div>

      <div class="examples-section">
        <div
          v-for="(category, index) in categories"
          :id="category.id"
          :key="index"
          class="category-group"
        >
          <h2 class="category-title">{{ category.name }}</h2>
          <div class="examples-grid">
            <div
              v-for="(example, exIndex) in category.examples"
              :key="exIndex"
              class="example-card"
            >
              <div class="card-header">
                <span>{{ example.title }}</span>
                <div class="actions">
                  <el-button
                    size="small"
                    :icon="CopyDocument"
                    title="复制代码"
                  />
                  <el-button size="small" :icon="Download" title="下载" />
                  <el-button size="small" :icon="FullScreen" title="全屏" />
                </div>
              </div>
              <div class="chart-container">
                <v-chart
                  :option="example.options"
                  autoresize
                  style="width: 100%; height: 100%"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { CopyDocument, Download, FullScreen } from '@element-plus/icons-vue'
import { ref, computed } from 'vue'
import { mixin_line } from './mixin_line'
// import 'echarts/lib/chart/line' vue2写法
// ECharts.compiled = echarts //多余代码
import VChart from 'vue-echarts' //6.0版本以上
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
])

const darkMode = ref < Boolean > false
const isEnglish = ref < Boolean > false
const currentLang = 'js'

const menuItems = ref([
  { id: 'line-chart', name: '折线图', icon: 'el-icon-s-data', langCount: 12 }
])

const darkModeIcon = computed(() => {
  return darkMode ? 'el-icon-sunny' : 'el-icon-moon'
})
const darkModeLabel = computed(() => {
  return darkMode ? '浅色模式' : '深色模式'
})
const currentLangBtn = computed(() => {
  return isEnglish ? '中文' : 'EN'
})
const currentLangLabel = computed(() => {
  return currentLang === 'js' ? 'JavaScript' : 'TypeScript'
})

const handleMenuSelect = (id) => {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

const categories = ref([
  {
    id: 'line-chart',
    name: '折线图',
    examples: [
      {
        title: '基础折线图',
        options: mixin_line.getLineChartOptions(
          '基础折线图',
          ['周一', '周二', '周三', '周四', '周五'],
          [120, 132, 101, 134, 90]
        )
      },
      {
        title: '基础平滑折线图',
        options: mixin_line.getSmoothedLineChartOptions(
          '基础平滑折线图',
          ['周一', '周二', '周三', '周四', '周五'],
          [120, 132, 101, 134, 90],
          true
        )
      },
      {
        title: '未来一周气温变化',
        options: mixin_line.getWeatherChartOptions()
      },
      {
        title: '基础面积图',
        options: mixin_line.getAreaChartOptions('基础面积图')
      },
      {
        title: '折线图堆叠',
        options: mixin_line.getStackedLineOptions()
      },
      {
        title: '堆叠面积图',
        options: mixin_line.getStackedAreaOptions()
      },
      {
        title: '渐变堆叠面积图',
        options: mixin_line.getGradientStackedAreaOptions()
      },
      // {
      //   title: '凹凸图',
      //   options: mixin_line.getBumpChartOptions()
      // },
      {
        title: '折线图区域高亮',
        options: mixin_line.getAreaPiecesOptions()
      },
      // {
      //   title: '数据过滤',
      //   options: mixin_line.getDataTransformFilterOptions()
      // },
      {
        title: '折线图的渐变',
        options: mixin_line.getLineGradientOptions()
      },
      {
        title: '一天用电量分布',
        options: mixin_line.getDistributionofElectricityOptions()
      },
      {
        title: '大数据量面积图',
        options: mixin_line.getLargescaleareachartOptions()
      },
      // {
      //   title: 'Confidence Band',
      //   options: mixin_line.getConfidenceBandOptions()
      // },
      {
        title: '雨量Evaporation关系图',
        options: mixin_line.getRainfallvsEvaporationOptions()
      },
      // {
      //   title: '北京 AQI 可视化',
      //   options: mixin_line.getBeijingAQIOptions()
      // },
      {
        title: '多 X 轴',
        options: mixin_line.getMultipleXAxesOptions()
      },
      {
        title: '雨量流量关系图',
        options: mixin_line.getRainfallOptions()
      },
      {
        title: '时间轴折线图',
        options: mixin_line.getAreaChartwithTimeAxisOptions()
      },
      {
        title: '动态数据 + 时间坐标轴',
        options: mixin_line.getDynamicData_TimeAxisOptions()
      },
      {
        title: '函数绘图',
        options: mixin_line.getFunctionPlotOptions()
      },
      // {
      //   title: '动态排序折线图',
      //   options: mixin_line.getLineRaceOptions()
      // },
      {
        title: '折线图的标记线',
        options: mixin_line.getLinewithMarklinesOptions()
      },
      {
        title: '自定义折线图样式',
        options: mixin_line.getLineStyleandItemStyleOptions()
      },
      {
        title: '双数值轴折线图',
        options: mixin_line.getLineChartinCartesianCoordinateOptions()
      },
      {
        title: '对数轴示例',
        options: mixin_line.getLogAxisOptions()
      },
      {
        title: '阶梯折线图',
        options: mixin_line.getStepLineOptions()
      },
      {
        title: '缓动函数可视化',
        options: mixin_line.getLineEasingVisualizingOptions()
      },
      {
        title: '垂直折线图（Y轴为类',
        options: mixin_line.getLineYCategoryOptions()
      },
      {
        title: '自定义图形组件',
        options: mixin_line.getCustomGraphicComponentOptions()
      },
      // {
      //   title: '点击添加折线图拐点',
      //   options: mixin_line.getClicktoAddPointsOptions()
      // },
      {
        title: '极坐标双数值轴',
        options: mixin_line.getTwoValue_AxesinPolar1Options()
      },
      {
        title: '极坐标双数值轴',
        options: mixin_line.getTwoValue_AxesinPolar2Options()
      },
      {
        title: '移动端上的 dataZoom ',
        options: mixin_line.getTooltipandDataZoomonMobileOptions()
      },
      {
        title: '可拖拽点',
        options: mixin_line.getDraggablePointsOptions()
      },
      {
        title: '联动和共享数据集',
        options: mixin_line.getShareDatasetOptions()
      }
    ]
  }
])
</script>

<style scoped>
/* .dashboard-container {
  //display: flex;
  height: 100%;
  width: 100%;
  //background-color: #f5f7fa;
  display: flex;
  //min-height: 100vh;
  //background-color: #f5f7fa;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', Arial, sans-serif;
} */

/* 左侧菜单样式 */
.menu {
  width: 240px;
  height: 100%;
  background-color: #fff;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
  border-right: 1px solid #e6e6e6;
}

/* 右侧内容区样式 */
.content {
  flex: 1;
  padding: 20px;
}

.echarts-container {
  width: 100%;
  height: 600px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

/* 菜单项选中样式 */
.el-menu-item.is-active {
  background-color: #ecf5ff;
  color: #409eff;
  font-weight: bold;
}

.menu-sidebar {
  width: 220px;
  height: 95%;
  /* //box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  //left: 50; */
  top: 5;
  bottom: 5;
  /* //min-height: 100vh; */
  background-color: #fff;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  position: fixed;
  z-index: 1000;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.logo {
  height: 60px;
  padding: 15px 20px;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
}

/* 
.menu {
  //border-right: none;
  flex: 1;
  border-right: none;
  padding: 10px 0;
} */

.content-container {
  flex: 1;
  margin-left: 220px;
  padding: 0;
  overflow-y: auto;
}

.header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 10;
}

.search-box {
  width: 300px;
}

.actions .el-button {
  margin-left: 10px;
}

.examples-section {
  padding: 20px;
}

.category-group {
  margin-bottom: 40px;
}

.category-title {
  font-size: 20px;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
  color: #1f2d3d;
}

.examples-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  grid-gap: 20px;
}

.example-card {
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.example-card:hover {
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transform: translateY(-3px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #e6e6e6;
  font-weight: 500;
}

.card-header .actions .el-button {
  padding: 4px;
  margin-left: 5px;
}

.chart-container {
  height: 280px;
  padding: 10px;
}
</style>
