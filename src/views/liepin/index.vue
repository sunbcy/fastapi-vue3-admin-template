<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <el-col
        :xs="{ span: 24 }"
        :sm="{ span: 24 }"
        :md="{ span: 24 }"
        :lg="{ span: 24 }"
        :xl="{ span: 24 }"
      >
        <!-- 上半部分内容 -->
        <div>
          <!--            class="grid-content bg-purple blur-background"-->
          <h2>查询</h2>
          <div>
            <el-input
              type="text"
              placeholder="输入职位"
              v-model="searchJobKeyword"
              class="custom-input"
              @keyup.enter="search"
            />
            <el-button type="primary" @click="search">搜索</el-button>
          </div>

          <div>
            <label for="region">选择地区：</label>
            <el-select id="region" v-model="selectedRegion">
              <el-option value="410">全国</el-option>
              <el-option
                v-for="(region, code) in regions"
                :key="region"
                :value="region"
                >{{ code }}</el-option
              >
            </el-select>
          </div>
        </div>
      </el-col>

      <el-col
        :xs="{ span: 24 }"
        :sm="{ span: 24 }"
        :md="{ span: 12 }"
        :lg="{ span: 12 }"
        :xl="{ span: 12 }"
      >
        <!-- 下面-左侧或上半部分内容 -->
        <div class="grid-content bg-purple blur-background">
          <h2>数据库概览</h2>
          <p>职位总数: {{ this.jobNum }}</p>
          <p>公司总数: {{ this.compNum }}</p>
        </div>
      </el-col>
      <el-col
        :xs="{ span: 24 }"
        :sm="{ span: 24 }"
        :md="{ span: 12 }"
        :lg="{ span: 12 }"
        :xl="{ span: 12 }"
      >
        <!-- 下面-右侧或下半部分内容 -->
        <div
          class="grid-content bg-purple-light blur-background long-cnt"
          ref="contentContainer"
          @scroll="handleScroll"
        >
          <h2>筛选</h2>
          <div>
            <el-button type="primary" @click="exportData"
              >导出为 JSON</el-button
            >
          </div>

          <div>
            <div class="search-results">
              <div
                class="card"
                v-for="result in searchResults"
                :key="result.id"
                @click="fetchDetails(result)"
              >
                <div>
                  <h3>
                    【{{ result.id }}】 {{ result.job_title }}
                    {{ result.job_dq }}
                  </h3>
                  <span class="job-salary">{{ result.job_salary }}</span>
                </div>
                <div>
                  <span class="label-tag">{{
                    result.job_requireWorkYears
                  }}</span>
                  <span class="label-tag">{{
                    result.job_requireEduLevel
                  }}</span>
                  <span class="label-tag">{{ result.job_labels }}</span>
                </div>
                <div>
                  <a
                    :href="result.comp_link"
                    class="company-info link-style"
                    target="_blank"
                  >
                    {{ result.compName }}</a
                  >
                  <span class="company-info"> {{ result.compIndustry }}</span>
                  <span class="company-info"> {{ result.compScale }}</span>
                </div>
                <a :href="result.job_link" class="link-style" target="_blank">{{
                  result.job_link
                }}</a>
              </div>
            </div>
          </div>

          <!-- 回到顶部按钮 -->
          <div
            class="back-to-top-container"
            v-show="showBackToTopButton"
            @click="scrollToTop"
          >
            <el-tooltip placement="top" content="回到顶部">
              <i class="el-icon-arrow-up"></i>
            </el-tooltip>
          </div>
        </div>
      </el-col>
    </el-row>

    <!--      <el-tooltip placement="top" content="ToTop">-->
    <!--        <back-to-top :custom-style="myBackToTopStyle" :visibility-height="300" :back-position="50" transition-name="fade" />-->
    <!--      </el-tooltip>-->

    <!-- 对话框组件 -->
    <el-dialog v-model:visible="dialogVisible" title="职位详情" width="87%">
      <p v-if="details && details.job_tags">{{ details.job_tags }}</p>
      <p
        v-if="details && details.job_intro_content"
        v-html="formattedJobDetailIntro"
      ></p>
      <p
        v-if="details && details.company_intro"
        v-html="formattedCompanyIntro"
      ></p>
      <p
        v-if="details && details.company_info"
        v-html="formattedCompanyInfo"
      ></p>
      <p v-else>加载中...</p>
    </el-dialog>
  </div>
</template>

<script setup>
import {
  search_jobs,
  get_job_num,
  get_comp_num,
  getJobDetails
} from '@/api/liepin'
// import BackToTop from '@/components/BackToTop'
import { saveAs } from 'file-saver'
import Blob from 'blob'
import { computed, onMounted, ref } from 'vue'
import { onBeforeUnmount } from 'vue'
import { ElMessage } from 'element-plus'
import { sanitizeHtml } from '@/utils/security'

const details = ref(null)
const dialogVisible = ref(false)
const jobNum = ref('')
const compNum = ref('')
const searchJobKeyword = ref('Python爬虫')
const searchResults = ref([])
const selectedRegion = ref('410')
const regions = ref({
  // 地区选项列表，键为地区名称，值为地区代码
  北京: '010',
  上海: '020',
  重庆: '040',
  广州: '050020',
  深圳: '050090',
  成都: '280020',
  杭州: '070020',
  南京: '060020',
  武汉: '170020',
  苏州: '060080'
  // 可根据实际需求添加更多地区选项
})
const myBackToTopStyle = ref({
  right: '50px',
  bottom: '50px',
  width: '40px',
  height: '40px',
  'border-radius': '4px',
  'line-height': '45px', // 请保持与高度一致以垂直居中 Please keep consistent with height to center vertically
  background: '#e7eaf1' // 按钮的背景颜色 The background color of the button
})
const dataToExport = ref({
  // 这里是你要导出的变量内容
  key: 'value'
})
const showBackToTopButton = ref(false)
const contentContainer = ref(null)

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

// 组件挂载时执行
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  setTimeout(getJobNum(), 300)
  getCompNum()
})

const fetchDetails = async (job) => {
  const reqData = {
    payload: {
      jobUrl: job.job_link,
      city: selectedRegion.value,
      dq: selectedRegion.value,
      currentPage: 0,
      key: searchJobKeyword.value,
      workYearCode: '0'
    }
  }
  dialogVisible.value = true
  try {
    const res = await getJobDetails(reqData)
    details.value = res.searchResults
    console.log('Details:', details.value) // 调试信息
    ElMessage.success(`获取职位信息✅`)
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常, 职位detail搜索失败')
  }
}

const getJobNum = async () => {
  try {
    const res = await get_job_num()
    jobNum.value = res.searchResults
    console.log(jobNum.value)
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常, 职位数目搜索失败')
  }
}

const getCompNum = async () => {
  try {
    const res = await get_comp_num()
    compNum.value = res.searchResults
    console.log(compNum.value)
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常, 公司数目搜索失败')
  }
}

const search = async () => {
  console.log('search ' + searchJobKeyword.value)
  const req_Data = {
    city: selectedRegion.value,
    dq: selectedRegion.value,
    currentPage: 0,
    key: searchJobKeyword.value,
    workYearCode: '0'
  }
  console.log(req_Data)
  try {
    const res = await search_jobs(req_Data)
    searchResults.value = res.searchResults
    dataToExport.value.key = res.searchResults
    // setTimeout(() => {
    //   this.searchResults = res.searchResults
    //   this.dataToExport.key = res.searchResults
    // }, 500)
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常, 职位搜索失败')
  }
}

const exportData = async () => {
  const jsonData = JSON.stringify(dataToExport, null, 2)
  const blob = new Blob([jsonData], { type: 'application/json' })
  // 文件名默认为搜索的职位名称加搜索时间
  const fileNamePrefix = searchJobKeyword.value
  // 创建一个新的 Date 对象以获取当前时间
  const now = new Date()

  // 定义一个函数来格式化日期
  function formatDate(date) {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0') // 月份从0开始，需要+1
    const day = String(date.getDate()).padStart(2, '0')
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    const seconds = String(date.getSeconds()).padStart(2, '0')

    // 返回格式化的日期字符串，例如：2024-09-24T20-20-20
    return `${year}-${month}-${day}T${hours}-${minutes}-${seconds}`
  }

  // 获取格式化后的搜索时间
  const searchTime = formatDate(now)
  // 构建完整的文件名
  const fileName = `${fileNamePrefix}_${searchTime}.json`
  saveAs(blob, fileName)
  ElMessage.success(`保存${fileName} at ${searchTime}✅`)
}

const handleScroll = async (event) => {
  const scrollTop = event.target.scrollTop
  if (scrollTop > 300) {
    // 当滚动距离超过300px时显示回到顶部按钮
    showBackToTopButton.value = true
  } else {
    showBackToTopButton.value = false
  }
}

const scrollToTop = async () => {
  if (contentContainer.value) {
    contentContainer.value.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }
}

const formattedJobDetailIntro = computed(() => {
  const rawContent = details.value?.job_intro_content || ''
  const withLineBreaks = rawContent.replace(/\r?\n/g, '<br>')
  return sanitizeHtml(withLineBreaks)
})

const formattedCompanyIntro = computed(() => {
  const rawContent = details.value?.company_intro || ''
  const withLineBreaks = rawContent.replace(/\r?\n/g, '<br>')
  return sanitizeHtml(withLineBreaks)
})

const formattedCompanyInfo = computed(() => {
  const rawContent = details.value?.company_info || ''
  const withLineBreaks = rawContent.replace(/\r?\n/g, '<br>')
  return sanitizeHtml(withLineBreaks)
})
</script>

<style lang="scss" scoped>
.grid-content {
  display: flex;
  flex-direction: column;
  //align-items: center;
  //justify-content: center;
  color: white;
  font-size: 12px;
  padding: 20px;
}

.long-cnt {
  height: 100%; /* 使内容区域占满可用空间 */
  overflow-y: auto; /* 添加垂直滚动条 */
}

.bg-purple {
  background-color: #99a9bf;
}

.bg-purple-light {
  background-color: #d3dce6;
}

.blur-background {
  backdrop-filter: blur(10px); /* 高斯模糊效果 */
  -webkit-backdrop-filter: blur(10px); /* Safari 和 Chrome 兼容 */
}

/* 桌面端样式 */
@media (min-width: 768px) {
  .grid-content {
    height: 100vh; /* 每个部分占据视口高度的一半 */
  }
}

/* 移动端样式 */
@media (max-width: 767px) {
  .grid-content {
    height: 50vh; /* 每个部分占据视口高度的一半 */
  }
}

.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}

.custom {
  &-input {
    width: 80%;
  }
}

.search-results {
  display: flex;
  flex-direction: column; /*卡片竖向排列 */
  // align-items: center;
}

.card,
.details-card {
  width: 80%;
  padding: 20px;
  margin: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card a {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis; // 防止url过长，显示异常
  white-space: nowrap;
}
.job-salary {
  flex-shrink: 0;
  margin-left: 12px;
  font-size: 18px;
  line-height: 25px;
  font-weight: bold;
  color: rgb(255, 100, 0);
}

.label-tag {
  margin-right: 8px;
  font-size: 12px;
  line-height: 22px;
  border-radius: 6px;
  padding: 0px 8px;
  color: rgb(102, 102, 102);
  background-color: rgb(248, 249, 251);
}

.company-info {
  flex-shrink: 0;
  max-width: 290px;
  padding-left: 8px;
  line-height: 17px;
  font-size: 12px;
  color: rgb(7, 19, 43);
}

h3 {
  margin: 0 0 10px;
}

p {
  margin: 0;
}

.link-style {
  text-decoration: none;
  color: #007bff;
  transition: color 0.3s, text-decoration 0.3s;
}

.link-style:hover {
  color: #0056b3;
  text-decoration: underline;
}

.back-to-top-container {
  position: fixed; /* 固定定位 */
  right: 20px; /* 距离右边 20px */
  bottom: 20px; /* 距离底部 20px */
  z-index: 1000; /* 确保按钮在其他元素之上 */
  cursor: pointer;
}

.back-to-top-container .el-tooltip__popper {
  background-color: #fff;
  border: 1px solid #ebeef5;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  color: #303133;
}
</style>
