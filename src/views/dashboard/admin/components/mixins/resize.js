import { onMounted, onBeforeUnmount, onActivated, onDeactivated } from 'vue'
import { debounce } from '@/utils'

export function useResizeHandler(chartRef) {
  // 创建响应式变量
  let sidebarElm = null
  let resizeHandler = null

  // 初始化 resize 事件
  const initResizeEvent = () => {
    window.addEventListener('resize', resizeHandler)
  }

  // 销毁 resize 事件
  const destroyResizeEvent = () => {
    window.removeEventListener('resize', resizeHandler)
  }

  // 侧边栏 resize 处理
  const sidebarResizeHandler = (e) => {
    if (e.propertyName === 'width') {
      resizeHandler()
    }
  }

  // 初始化侧边栏 resize 事件
  const initSidebarResizeEvent = () => {
    sidebarElm = document.getElementsByClassName('sidebar-container')[0]
    if (sidebarElm) {
      sidebarElm.addEventListener('transitionend', sidebarResizeHandler)
    }
  }

  // 销毁侧边栏 resize 事件
  const destroySidebarResizeEvent = () => {
    if (sidebarElm) {
      sidebarElm.removeEventListener('transitionend', sidebarResizeHandler)
    }
  }

  // 创建防抖 resize 处理器
  resizeHandler = debounce(() => {
    if (chartRef.value) {
      chartRef.value.resize()
    }
  }, 100)

  // 生命周期钩子
  onMounted(() => {
    initResizeEvent()
    initSidebarResizeEvent()
  })

  onBeforeUnmount(() => {
    destroyResizeEvent()
    destroySidebarResizeEvent()
  })

  // keep-alive 相关钩子
  onActivated(() => {
    initResizeEvent()
    initSidebarResizeEvent()
  })

  onDeactivated(() => {
    destroyResizeEvent()
    destroySidebarResizeEvent()
  })
}
