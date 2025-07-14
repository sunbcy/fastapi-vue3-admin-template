import { cloneDeep as _cloneDeep } from 'lodash-es'

/**
 * @method menuListSort
 * @param {*} data
 * @returns
 */
export const menuListSort = (data) => {
  const sortedList = _cloneDeep(data)

  sortedList.sort((a, b) => b.sort - a.sort)

  sortedList.forEach((item) => {
    if (item.children) {
      item.children = menuListSort(item.children)
    }
  })

  return sortedList
}

/**
 * @method findItemWithPath
 * @param {*} data
 * @returns
 */
export const findItemWithPath = (data) => {
  for (let i = 0; i < data.length; i++) {
    const item = data[i]

    if (item.type === 1) {
      return item.path
    } else if (item.children && item.children.length > 0) {
      const foundPath = findItemWithPath(item.children)

      if (foundPath) {
        return item.path + '/' + foundPath
      }
    }
  }
}

/**
 * @method convertToTree
 * @param {*} nodes
 * @param {*} parentId
 * @returns
 */
export const convertToTree = (nodes, parentId = 0) => {
  const result = []

  for (const node of nodes) {
    if (node.parentId === parentId) {
      const newNode = { ...node }

      const children = convertToTree(nodes, node.id)

      newNode.children = children

      result.push(newNode)
    }
  }
  return result
}

/**
 * 高级防抖函数 - 支持即时调用、取消功能、返回值处理和 Promise 支持
 *
 * @param {Function} func - 要执行的目标函数
 * @param {number} [wait=300] - 等待时间（毫秒）
 * @param {Object} [options={}] - 配置选项
 * @param {boolean} [options.leading=false] - 是否在等待开始前立即调用
 * @param {boolean} [options.trailing=true] - 是否在等待结束后调用
 * @param {boolean} [options.returnPromise=false] - 是否返回 Promise
 *
 * @returns {Function} - 防抖处理后的函数（带 cancel 方法）
 */
export function debounce(func, wait = 300, options = {}) {
  // 默认配置
  const { leading = false, trailing = true, returnPromise = false } = options

  let timeoutId = null
  let lastArgs = null
  let lastThis = null
  let lastCallTime = null
  let result = null
  let resolveList = []

  // 清理函数
  function clear() {
    if (timeoutId) {
      clearTimeout(timeoutId)
      timeoutId = null
    }
  }

  // 结束调用处理
  function complete() {
    if (trailing && lastArgs) {
      result = func.apply(lastThis, lastArgs)

      // 处理 Promise 解析
      resolveList.forEach((resolve) => resolve(result))
      resolveList = []
    }
  }

  // 延迟函数
  function later() {
    const elapsed = Date.now() - lastCallTime

    if (elapsed < wait && elapsed >= 0) {
      // 时间未到，继续等待剩余时间
      timeoutId = setTimeout(later, wait - elapsed)
    } else {
      // 时间已到，完成调用
      clear()
      complete()
    }
  }

  // 防抖主函数
  function debounced(...args) {
    lastCallTime = Date.now()
    lastArgs = args
    lastThis = this

    clear()

    // 立即调用处理
    const shouldCallNow = leading && !timeoutId

    // 设置定时器
    timeoutId = setTimeout(later, wait)

    if (shouldCallNow) {
      result = func.apply(lastThis, lastArgs)

      // 处理 Promise 解析
      if (returnPromise) {
        const promise = Promise.resolve(result)
        resolveList.forEach((resolve) => resolve(result))
        resolveList = []
        return promise
      }
      return result
    }

    // 处理 Promise 返回值
    if (returnPromise) {
      return new Promise((resolve) => {
        resolveList.push(resolve)
      })
    }

    return result
  }

  // 添加取消方法
  debounced.cancel = function () {
    clear()
    lastArgs = null
    lastThis = null

    // 拒绝所有未完成的 Promise
    if (returnPromise) {
      resolveList.forEach((resolve) => resolve())
      resolveList = []
    }
  }

  // 添加立即执行方法
  debounced.flush = function () {
    clear()
    return complete()
  }

  return debounced
}
