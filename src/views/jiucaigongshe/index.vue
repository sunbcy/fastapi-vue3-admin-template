<template>
  <div class="jiucaigongshe-container">
    <div>
      <div class="search-results">
        <div v-for="result in searchResults" :key="result.id" class="card">
          <h3>{{ result.id }}</h3>
          <!--                <p>{{ result.url_title }}</p>-->
          <div
            v-for="sub_result in result.url_title"
            :key="sub_result.code"
            class="card"
          >
            <h4>
              <span class="stock-num">{{ sub_result.code }}</span>
              {{ sub_result.name }}
            </h4>
            <!--                  <p>{{ sub_result.article }}</p>-->
            <p>最新价：{{ sub_result.article.action_info.price / 100 }}</p>
            <p>
              涨跌幅：<span style="color: red"
                >{{ sub_result.article.action_info.shares_range / 100 }} %</span
              >
            </p>
            <p>涨停时间：{{ sub_result.article.action_info.time }}</p>
            <!--                  <div v-html="formattedDynamicMessage"></div>-->
            <!--                  <p>解析：{{ sub_result.article.action_info.expound }}</p>-->
            解析：
            <div v-html="formatExpound(sub_result)" />
          </div>
        </div>
      </div>
    </div>
    <el-tooltip placement="top" content="ToTop">
      <back-to-top
        :custom-style="myBackToTopStyle"
        :visibility-height="300"
        :back-position="50"
        transition-name="fade"
      />
    </el-tooltip>
  </div>
</template>

<script setup>
import { get_block_info } from '@/api/jiucaigongshe'
import BackToTop from '@/components/BackToTop'
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'

const searchResults = ref([])
const myBackToTopStyle = ref({
  right: '50px',
  bottom: '50px',
  width: '40px',
  height: '40px',
  'border-radius': '4px',
  'line-height': '45px', // 请保持与高度一致以垂直居中 Please keep consistent with height to center vertically
  background: '#e7eaf1' // 按钮的背景颜色 The background color of the button
})

const get_info = async () => {
  try {
    const res = await get_block_info()
    searchResults.value = res.searchResults
    console.log(searchResults.value)
    ElMessage.success(`获取A股信息✅`)
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常，git pull 失败')
  }
}

const formatExpound = (sub_result) => {
  // 确保sub_result.article.action_info.expound存在
  if (
    sub_result &&
    sub_result.article &&
    sub_result.article.action_info &&
    sub_result.article.action_info.expound
  ) {
    return sub_result.article.action_info.expound.replace(/\n/g, '<br>')
  }
  return '' // 如果不存在，则返回空字符串
}

// 组件挂载时执行
onMounted(() => {
  get_info()
})
</script>

<style lang="scss" scoped>
.jiucaigongshe {
  &-container {
    margin: 5px;
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

.stock-num {
  font-weight: bold;
  font-size: 12px;
  color: #888;
}

.search-results {
  display: flex;
  flex-direction: column; /*卡片竖向排列 */
  // align-items: center;
}

.card {
  //width: 98%;
  padding: 5px;
  margin: 3px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h3 {
  margin: 0 0 10px;
}

p {
  margin: 0;
}
</style>
