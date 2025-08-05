<template>
  <el-card class="preprocess-card">
    <h3>预处理结果</h3>
    <el-collapse accordion>
      <!-- 原始HTML带高亮 -->
      <el-collapse-item title="原始HTML" name="html">
        <pre
          class="html-preview"
        ><code class="language-html">{{ purifiedHtml }}</code></pre>
        <el-button @click="copyHtml">复制HTML</el-button>
      </el-collapse-item>

      <!-- 清洗文本带收起功能 -->
      <el-collapse-item
        title="清洗后文本"
        name="text"
        :disabled="data.clean_text.length > 5000"
      >
        <el-scrollbar height="150px">
          {{ data.clean_text }}
        </el-scrollbar>
      </el-collapse-item>

      <!-- 分词结果带交互 -->
      <el-collapse-item title="分词结果" name="tokens">
        <div class="token-container">
          <el-tag
            v-for="(word, index) in data.tokens"
            :key="index"
            class="token-tag"
            :type="getTagType(word)"
            @mouseenter="showPopover(word, index)"
            @mouseleave="popoverVisible = false"
          >
            {{ word }}
            <el-popover
              placement="top"
              :title="`词性: ${currentPos}`"
              trigger="manual"
              v-model:visible="popoverVisible"
            >
              <p>当前分析: {{ currentWord }}</p>
            </el-popover>
          </el-tag>
        </div>
        <el-statistic title="总词数" :value="data.tokens.length" />
      </el-collapse-item>
    </el-collapse>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import DOMPurify from 'dompurify'
import Prism from 'prismjs'

const currentWord = ref('')
const currentPos = ref('')
const popoverVisible = ref(false)

const showPopover = (word, index) => {
  currentWord.value = word
  currentPos.value = getPOS(word)
  popoverVisible.value = true
}

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

// 1. HTML净化与高亮
const purifiedHtml = computed(() => {
  const clean = DOMPurify.sanitize(props.data.original_html)
  return Prism.highlight(clean, Prism.languages.html, 'html')
})

// 2. 词性标注逻辑
const activeIndex = ref(null)
const getPOS = (word) => {
  // 实际接入NLP服务
  return '名词'
}

// 3. 高频词标签类型
const getTagType = (word) => {
  const freq = props.data.tokens.filter((w) => w === word).length
  return freq > 3 ? 'danger' : 'success'
}

// 4. 复制功能
const copyHtml = () => {
  navigator.clipboard.writeText(props.data.original_html)
}
</script>

<style scoped>
.preprocess-card {
  margin: 20px 0;
}
.html-preview {
  background: #2d2d2d;
  color: #f8f8f2;
  padding: 15px;
  border-radius: 4px;
  max-height: 300px;
  overflow: auto;
}
.token-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}
.token-tag {
  cursor: pointer;
  transition: transform 0.2s;
}
.token-tag:hover {
  transform: translateY(-3px);
}
</style>
