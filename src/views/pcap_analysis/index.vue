<template>
  <el-container>
    <el-header>数据包上传 & 分析结果</el-header>
    <el-main>
      <el-row :gutter="20">
        <!-- 文件上传的列 -->
        <el-col :span="12">
          <div class="upload-container">
            <el-upload
              ref="uploadRef"
              class="upload"
              drag
              :action="uploadUrl"
              :on-progress="handleProgress"
              :on-success="handleSuccess"
              :on-error="handleError"
              :file-list="fileList"
              multiple
            >
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="upload-tip">将文件拖至此处，或<em>点击上传</em></div>
              <el-button size="small" type="primary">选取文件</el-button>
            </el-upload>
            <!-- 进度条 -->
            <el-progress
              v-show="uploadPercentage > 0"
              :percentage="uploadPercentage"
            />
            <el-button
              type="success"
              :disabled="!fileList.length || isUploading"
              @click="startAnalysis"
              >开始分析</el-button
            >
          </div>
        </el-col>

        <!-- 分析结果的列 -->
        <el-col :span="12">
          <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="id" label="ID" width="180" />
            <el-table-column prop="packetName" label="数据包名" width="180" />
            <el-table-column label="分析结果链接" width="180">
              <template #default="scope">
                <el-link @click="showResultDialog(scope.row.id)"
                  >查看结果</el-link
                >
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </el-main>
  </el-container>

  <!-- 对话框组件 -->
  <el-dialog v-model="dialogVisible" title="详细结果" width="60%">
    <Result
      :id="currentId"
      :table-data="tableData"
      @close="dialogVisible = false"
    />
  </el-dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { get_analysis_info } from '@/api/pcap_analysis'
import Result from './Result.vue'

// 常量配置
const uploadUrl = import.meta.env.VITE_BASE_API + '/pcap_analysis/upload'

// 响应式数据
const fileList = ref([])
const uploadPercentage = ref(0)
const isUploading = ref(false)
const tableData = ref([])
const dialogVisible = ref(false)
const currentId = ref('')
const uploadRef = ref(null)

// 生命周期钩子
onMounted(() => {
  // 当组件被加载后，获取分析数据
  startAnalysis()
})

// 事件处理函数
const handleProgress = (event) => {
  uploadPercentage.value = Math.floor(event.percent || 0)
}

const handleSuccess = (response) => {
  ElMessage.success('文件上传成功')
  uploadPercentage.value = 0
  isUploading.value = false

  // 更新文件列表
  if (response.data?.fileNames) {
    fileList.value = [
      ...fileList.value,
      ...response.data.fileNames.map((name) => ({ name }))
    ]
  }
}

const handleError = (error) => {
  ElMessage.error(`文件上传失败: ${error.message || '未知错误'}`)
  uploadPercentage.value = 0
  isUploading.value = false
}

const showResultDialog = (id) => {
  currentId.value = id
  dialogVisible.value = true
}

// 核心方法
const getAnalysisData = async () => {
  try {
    const sendData = { data: fileList.value.map((file) => file.name) }
    const res = await get_analysis_info(sendData)

    if (res.code === 200) {
      tableData.value = res.data
    } else {
      ElMessage.warning(`分析失败: ${res.message || '未知错误'}`)
    }
  } catch (err) {
    console.error('分析异常:', err)
    ElMessage.error('服务端异常, 分析失败.')
  }
}

const startAnalysis = () => {
  if (fileList.value.length > 0) {
    ElMessage.success('开始分析数据包...')
    isUploading.value = true
    getAnalysisData()
  } else {
    ElMessage.warning('请先上传数据包')
  }
}
</script>

<style scoped>
.upload-container {
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  padding: 40px 20px;
  text-align: center;
  transition: border-color 0.3s;
}

.upload-container:hover {
  border-color: #409eff;
}

.upload-tip em {
  color: #409eff;
  cursor: pointer;
}

.el-progress {
  margin-top: 20px;
}

.el-button {
  margin-top: 20px;
}
</style>
