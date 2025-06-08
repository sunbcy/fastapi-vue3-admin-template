<template>
  <div>
    <h3>Code Editor</h3>
    <div style="width: 500px">
      <el-input v-model="filename" placeholder="input filename"></el-input>
      <el-button type="primary" @click="save_file">Save</el-button>
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

<script>
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

export default {
  name: 'CodeEditor',
  components: {
    Codemirror
  },
  data() {
    return {
      filename: 'test.py',
      code: 'console.log("Hello, World!");\nconsole.log("Test Line 2!");',
      cmOptions: {
        mode: 'python',
        theme: 'default',
        lineNumbers: true,
        lineWrapping: true,
        viewportMargin: Infinity
      },
      clientHeight: 0, // 修复3：声明响应式高度
      editor: null // 修复3：声明编辑器引用
    }
  },
  mounted() {
    this.clientHeight = `${document.documentElement.clientHeight}`
    this.editor = this.$refs.cmEditor.editor // 修复4：正确访问编辑器实例
    // this.editor.setSize('auto', this.clientHeight - 205)

    window.addEventListener('resize', this.handleResize) // 修复2：添加事件监听
  },
  beforeUnmount() {
    // 修复2：生命周期钩子更名
    window.removeEventListener('resize', this.handleResize)
  },
  methods: {
    handleResize() {
      // 修复2：提取为独立方法
      this.clientHeight = `${document.documentElement.clientHeight}`
      // this.editor.setSize('auto', parseFloat(this.clientHeight) - 205)
    },
    save_file() {
      const reqData = {
        filename: this.filename,
        code: this.code
      }
      save_code(reqData)
        .then((res) => {
          if (res.code === 20000) {
            ElMessage.success(`${this.filename} 保存成功!`) // 修复1：使用新消息API
          } else {
            ElMessage.error(`${this.filename} 保存失败`)
          }
        })
        .catch(() => {
          ElMessage.error('服务端异常, 保存失败...')
        })
    }
  }
}
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
