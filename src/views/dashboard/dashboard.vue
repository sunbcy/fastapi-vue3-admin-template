<template>
  <div class="dashboard-container">
    <span v-html="formattedQuote"></span>

    <div class="button-container">
      <el-button type="primary" @click="updateProject">项目更新</el-button>
      <el-button type="primary" @click="compileProject">项目编译</el-button>
      <el-button type="primary" @click="restartProject">项目重启</el-button>
      <el-button type="danger" @click="oneClickRestart">一键重启</el-button>
    </div>

    <component :is="currentRole" />

    <el-card>
      <h3>System Information</h3>
      <p><strong>Current Time:</strong> {{ currentTime }}</p>
      <p><strong>System Type:</strong> {{ osType }}-{{ systemType }}</p>
      <p><strong>User Agent:</strong> {{ userAgent }}</p>
      <strong>CPU Info:</strong>
      <p v-html="formattedCPUInfo"></p>
      <strong>Disk Info:</strong>
      <p v-html="formattedInfo"></p>
      <p><strong>Local IP:</strong> {{ localIP }}</p>
      <p><strong>Wan IP:</strong> {{ wanIP }}</p>
      <p>
        <strong>Latitude, Longitude:</strong> [{{ Latitude }}, {{ Longitude }}]
      </p>
      <strong>IpInfo:</strong>
      <p v-html="formattedIpInfo"></p>
      <p><strong>Location:</strong> {{ Location }}</p>
    </el-card>
  </div>
</template>

<script setup name="Dashboard">
import adminDashboard from './admin'
import { get_system_info } from '@/api/system_info'
import { update_project } from '@/api/system_info'
import { compile_project } from '@/api/system_info'
import { restart_project } from '@/api/system_info'
import { getTodayQuote } from '@/api/azquotes'
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import os from 'os'

const todayQuote = ref('')
const currentTime = ref('')
const systemType = ref('')
const userAgent = ref('')
const cpuInfo = ref('')
const diskInfo = ref('')
const localIP = ref('')
const osType = ref('')
const wanIP = ref('')
const Latitude = ref('')
const Longitude = ref('')
const IpInfo = ref('')
const Location = ref('')
const currentRole = ref('adminDashboard')

onMounted(() => {
  updateTime()
  getSystemInfo()
  getQuote()
})

const updateProject = async () => {
  try {
    ElMessage.success(`执行 git pull`)
    const res = await update_project() // 序列化为 JSON 字符串 JSON.stringify(
    console.log(res.searchResults)
    ElMessage.success(`更新项目✅`)
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常，git pull 失败')
  }
}

const compileProject = async () => {
  try {
    ElMessage.success(`执行 npm run build:prod`)
    const res = await compile_project() // 序列化为 JSON 字符串 JSON.stringify(
    console.log(res.searchResults)
    ElMessage.success(`编译项目✅`)
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常，npm run build:prod 失败')
  }
}

const restartProject = async () => {
  try {
    ElMessage.success(`重启项目`)
    const res = await restart_project() // 序列化为 JSON 字符串 JSON.stringify(
    console.log(res.searchResults)
    ElMessage.success(`更新项目✅`)
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常，restart 失败')
  }
}

const oneClickRestart = async () => {
  try {
    ElMessage.success(`(未完成❎)执行 一键重启`)
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常， 一键重启 失败')
  }
}

const updateTime = async () => {
  try {
    currentTime.value = new Date().toLocaleString()
    setInterval(() => {
      currentTime.value = new Date().toLocaleString()
    }, 1000)
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常，git pull 失败')
  }
}

const getSystemInfo = async () => {
  // const os = require('os')
  const platform = navigator?.platform || ''
  systemType.value = platform.toLowerCase() // os.type()
  userAgent.value = navigator.userAgent
  try {
    const res = await get_system_info()
    osType.value = res.searchResults.os_type
    cpuInfo.value = res.searchResults.cpu_info
    diskInfo.value = res.searchResults.disk_info
    localIP.value = res.searchResults.local_ip
    wanIP.value = res.searchResults.wan_ip
    Latitude.value = res.searchResults.latitude
    Longitude.value = res.searchResults.longitude
    IpInfo.value = res.searchResults.ip_info
    Location.value = res.searchResults.location
    if (wanIP.value === 'ip not found!') {
      ElMessage.success(`服务器可能处于离线模式！请检查网络。。。`)
    }
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常，获取系统信息 失败')
  }
}

const getQuote = async () => {
  try {
    const res = await getTodayQuote() // 序列化为 JSON 字符串 JSON.stringify(
    todayQuote.value = res.searchResults.text
  } catch (error) {
    console.error('API请求异常：', error)
    ElMessage.error('服务端异常，获取quote 失败')
  }
}

const formattedQuote = computed(() => todayQuote.value.replace(/\n/g, '<br>'))
const formattedInfo = computed(() => diskInfo.value.replace(/\n/g, '<br>'))
const formattedIpInfo = computed(() => IpInfo.value.replace(/\n/g, '<br>'))
const formattedCPUInfo = computed(() => cpuInfo.value.replace(/\n/g, '    '))
</script>

<style lang="scss">
.dashboard-container {
  margin: 20px;
  background-color: #fff;
  padding: 20px;
}
</style>
