<template>
  <div class="sidebar-logo-container" :class="{ menuCollapse: menuCollapse }">
    <transition name="sidebarLogoFade">
      <router-link
        v-if="menuCollapse"
        key="menuCollapse"
        class="sidebar-logo-link"
        to="/"
      >
        <img v-if="logo" :src="logo" class="sidebar-logo" />
        <h1 v-else class="sidebar-title">{{ $t('title') }}</h1>
      </router-link>
      <router-link v-else key="expand" class="sidebar-logo-link" to="/">
        <img v-if="logo" :src="logo" class="sidebar-logo" />
        <h1 class="sidebar-title">{{ $t('title') }}</h1>
      </router-link>
    </transition>
  </div>
</template>

<script setup>
import { reactive, toRefs, computed } from 'vue'
import { useSettingsStore } from '@/store/settings'

const state = reactive({
  logo: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjgiIGhlaWdodD0iMTI4IiB2aWV3Qm94PSIwIDAgNjQgNjQiPjxwYXRoIGZpbGw9IiNkYzYwM2EiIGQ9Ik0xMy44MjUgNTkuMjljNi4xMzIgMi40MjIgMTQuNDMyIDQuOTQxIDIxLjA1IDQuMzQ5YzkuNjQ2LS44NjMgMjguNDk2LTQuODI3IDI4LjQ5Ni0yMS40MTRjMC0uMTYxLS4zODUtMS4zNjMtLjUxOC0xLjQxYy0uNzczLTIuMDEtMS42ODgtMy44MTUtMy4wMy01LjcwNGMtMS43ODMtMi41MTUtMy42Ni0xMS44NTMtMi41OC0xNC44NTljLjA2Mi0uMTY5LS4yNzctLjMxOC0uNDI4LS4zMWMtMy44NjMuMjYzLTcuNTc4IDYuMDYtOC4wMiA5LjM4OEMzNi4wMDMgMTUuMDc3IDM4Ljg1MSAzLjI3IDQwLjc3NS4zODFhLjEuMSAwIDAgMCAuMDI5LS4wOTVjLjAwMi0uMTc2LS4zNDYtLjM1Mi0uNTIzLS4yNjNjLTEyLjIxMyAyLjM0LTI2Ljk4NCAyNC40MDMtMjYuMjggMjcuNzE0Yy0yLjU0OS0xLjYyMi0uODg5LTEwLjM2Mi4wNjItMTIuODE4Yy4wNzgtLjE5OS0uMzgxLS4zODUtLjU0Ni0uMjc1Yy0yLjc1MiAxLjgyNS03LjExNiA3LjA4LTExLjczMiAyMC44NDNzNS42NDkgMjEuMjcxIDEyLjA0IDIzLjgwMyIvPjxwYXRoIGZpbGw9IiNmMWVhMzciIGQ9Ik01NS4wMyAzOC4zOWMtLjgwOSAzLjEwOC0xLjI4MSA2LjU4OS01Ljc2NiA3LjU1Yy03LjU1OSAxLjYyNi0zLjYyOS05Ljk1MS0zLjk0My0xMi43NDJjLS41MzEtNC42MjgtNS41NjItNy44LTEwLjcyOS05LjUzNmMtLjIwMS0uMDY4IDUuOTI2IDguMDItMy40NjQgOS45NTZjLTIuOTI4LjYwNS01LjgzOS0uOTctNi4yNTktMy41MzZjLS4xOTUtMS4yMjQuNDYxLTQuNzkzLjIyLTQuNjI0Yy0yLjMxNiAxLjYwNS00LjYxMSAzLjQyMS00Ljg3NCA1LjkzN2MtLjE2OSAxLjY3My42NjUgMy40ODUgMS4wMSA1LjEyYy41NTkgMi42OTMtLjQ3OSA0LjkyLTQuNDQyIDQuOTQ2Yy00Ljg3LjAyOS0zLjQxNy04LjUwOC0zLjQyNi04LjQ4N2MtLjA5OS0uMDgtMTguNDM1IDE3LjE1IDkuMjgzIDI5LjEyYzguMDcgMy40ODUgMjEuODA4LjkxNSAyOC43NTMtMy41MTljOS01Ljc0NiA0LjIyMy0yMi40NDcgMy42MzktMjAuMTkiLz48L3N2Zz4='
})

const { logo } = toRefs(state)

const settingsStore = useSettingsStore()
const menuBackgroundColor = computed(() => settingsStore.menuBackgroundColor)

defineProps({
  // 侧边栏展开状态
  menuCollapse: {
    type: Boolean,
    required: true
  }
})
</script>

<style lang="scss" scoped>
.sidebarLogoFade-enter-active {
  transition: opacity 1.5s;
}

.sidebarLogoFade-enter-from,
.sidebarLogoFade-leave-to {
  opacity: 0;
}

.sidebar-logo-container {
  position: relative;
  width: 100%;
  height: 50px;
  line-height: 50px;
  background: v-bind(menuBackgroundColor);
  text-align: center;
  overflow: hidden;

  & .sidebar-logo-link {
    height: 100%;
    width: 100%;

    & .sidebar-logo {
      width: 32px;
      height: 32px;
      vertical-align: middle;
      margin-right: 12px;
    }

    & .sidebar-title {
      display: inline-block;
      margin: 0;
      color: #fff;
      font-weight: 600;
      line-height: 50px;
      font-size: 12px;
      font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
      vertical-align: middle;
    }
  }

  &.menuCollapse {
    .sidebar-logo {
      margin-right: 0px;
    }
  }
}
</style>
