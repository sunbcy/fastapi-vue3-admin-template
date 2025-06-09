<!--suppress JSAnnotator -->
<template>
  <div>
    <h3>Code Editor</h3>
    <div style="width: 500px">
      <el-input v-model="filename" placeholder="input filename"></el-input>
      <el-button type="primary" @click="saveFile">Save</el-button>
    </div>
    <div class="editor-container">
      <Codemirror
        ref="cmEditor"
        v-model:value="code"
        :options="cmOptions"
        border
        height="600px"
      ></Codemirror>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage } from 'element-plus' // 修复1：引入消息组件
import Codemirror from 'codemirror-editor-vue3'
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/3024-day.css'
import 'codemirror/theme/ayu-mirage.css'
import 'codemirror/theme/monokai.css'
import 'codemirror/theme/rubyblue.css'

import 'codemirror/mode/htmlmixed/htmlmixed'
import 'codemirror/mode/javascript/javascript'
import 'codemirror/mode/python/python'
import { save_code } from '@/api/code_editor'

const filename = ref('test.py')
const code = ref('console.log("Hello, World!");\nconsole.log("Test Line 2!");')
const cmEditor = ref(null) // 编辑器实例引用
const clientHeight = ref(window.innerHeight)

// 编辑器配置
const cmOptions = ref({
  mode: 'python',
  theme: 'default',
  lineNumbers: true,
  lineWrapping: true,
  viewportMargin: Infinity
})

// 初始化编辑器
onMounted(() => {
  if (cmEditor.value) {
    const editor = cmEditor.value.editor
    // editor.setSize('auto', clientHeight.value - 205)
    window.addEventListener('resize', handleResize)
  }
})

// 清理资源
onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})

// 响应窗口大小变化
const handleResize = () => {
  clientHeight.value = window.innerHeight
  if (cmEditor.value?.editor) {
    // cmEditor.value.editor.setSize('auto', clientHeight.value - 205)
  }
}

// 保存文件逻辑
async function saveFile() {
  const reqData = {
    filename: filename.value,
    code: code.value
  }
  try {
    const res = await save_code(reqData) // 序列化为 JSON 字符串 JSON.stringify(
    // const res = JSON.parse(jsonString)
    console.log(res)

    if (res.code === 20000) {
      ElMessage.success(`${filename.value} 保存成功！`)
    } else {
      ElMessage.error(`${filename.value} 保存失败（错误码：${res.code}）`)
    }
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常，保存失败')
  }
}

// export default {
//   name: 'CodeEditor',
//   components: {
//     Codemirror
//   },
//
//   methods: {
//     // handleResize() {
//     //   // 修复2：提取为独立方法
//     //   this.clientHeight = `${document.documentElement.clientHeight}`
//     //   // this.editor.setSize('auto', parseFloat(this.clientHeight) - 205)
//     // },
//     const saveFile = async () =>{
//       const reqData = {
//         filename: filename.value,
//         code: code.value
//       }
//
//       try {
//         const res = await save_code(reqData) // 改用async/await语法
//         console.log('响应数据:', res)
//
//         if (res.code === 20000) {
//           ElMessage.success(`${filename.value} 保存成功!`) // 直接使用变量名
//         } else {
//           ElMessage.error(`${filename.value} 保存失败，错误码: ${res.code}`)
//         }
//       } catch (error) {
//         console.error('请求异常:', error)
//         ElMessage.error('服务端异常，保存失败...')
//       }
//
//     }
//   }
// }
</script>

<style scoped>
.editor-container {
  height: 600px;
}

/* 修复5：深度选择器语法 */
:deep(.cm-editor) {
  height: 100%;
}
</style>
