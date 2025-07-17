// src/utils/security.js
import DOMPurify from 'dompurify'

// 自定义钩子函数增强安全性
const hooks = {
  uponSanitizeElement: (node, data) => {
    // 移除所有事件处理器
    Array.from(node.attributes).forEach((attr) => {
      if (attr.name.startsWith('on')) {
        node.removeAttribute(attr.name)
      }
    })

    // 特殊处理链接
    if (data.tagName === 'a') {
      const href = node.getAttribute('href') || ''
      if (
        !href.startsWith('http://') &&
        !href.startsWith('https://') &&
        !href.startsWith('mailto:') &&
        !href.startsWith('tel:') &&
        !href.startsWith('#') &&
        !href.startsWith('/')
      ) {
        node.removeAttribute('href')
      } else {
        // 添加 rel="noopener noreferrer" 防止钓鱼攻击
        node.setAttribute('rel', 'noopener noreferrer')
        // 在新标签页打开外部链接
        if (href.startsWith('http')) {
          node.setAttribute('target', '_blank')
        }
      }
    }

    // 特殊处理图片
    if (data.tagName === 'img') {
      const src = node.getAttribute('src') || ''
      if (
        !src.startsWith('http://') &&
        !src.startsWith('https://') &&
        !src.startsWith('data:image/') &&
        !src.startsWith('/')
      ) {
        node.removeAttribute('src')
      }
    }
  },

  uponSanitizeAttribute: (node, data) => {
    // 移除所有内联样式
    if (data.attrName === 'style') {
      node.removeAttribute('style')
      return false // 阻止默认处理
    }

    // 移除危险属性
    const dangerousAttributes = [
      'onload',
      'onerror',
      'onclick',
      'onmouseover',
      'onfocus',
      'onblur',
      'onchange',
      'onsubmit',
      'onkeydown',
      'onkeypress',
      'onkeyup',
      'onmousedown',
      'onmousemove',
      'onmouseout',
      'onmouseup',
      'onreset',
      'onselect',
      'onunload',
      'onabort',
      'ondblclick',
      'ondrag',
      'ondragend',
      'ondragenter',
      'ondragleave',
      'ondragover',
      'ondragstart',
      'ondrop',
      'onresize',
      'onscroll'
    ]

    if (dangerousAttributes.includes(data.attrName)) {
      node.removeAttribute(data.attrName)
      return false // 阻止默认处理
    }

    // 移除 data: URL 协议（可能包含恶意脚本）
    if (data.attrName === 'src' && data.attrValue.startsWith('data:')) {
      // 只允许图片类型的 data URL
      if (!data.attrValue.startsWith('data:image/')) {
        node.removeAttribute(data.attrName)
        return false
      }
    }
  }
}

// 默认安全配置
const defaultConfig = {
  ALLOWED_TAGS: [
    'a',
    'b',
    'blockquote',
    'br',
    'caption',
    'code',
    'dd',
    'del',
    'div',
    'dl',
    'dt',
    'em',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'hr',
    'i',
    'img',
    'ins',
    'kbd',
    'li',
    'ol',
    'p',
    'pre',
    'q',
    's',
    'small',
    'span',
    'strike',
    'strong',
    'sub',
    'sup',
    'table',
    'tbody',
    'td',
    'tfoot',
    'th',
    'thead',
    'tr',
    'u',
    'ul'
  ],
  ALLOWED_ATTR: [
    'href',
    'src',
    'alt',
    'title',
    'width',
    'height',
    'align',
    'class',
    'id',
    'colspan',
    'rowspan',
    'border',
    'cellpadding',
    'cellspacing'
  ],
  ALLOW_DATA_ATTR: false,
  FORBID_TAGS: [
    'style',
    'script',
    'iframe',
    'object',
    'embed',
    'form',
    'input',
    'textarea',
    'button'
  ],
  FORBID_ATTR: ['style', 'on*'],
  ADD_ATTR: ['target', 'rel'], // 允许我们添加的 target 和 rel 属性
  ADD_TAGS: [],
  WHOLE_DOCUMENT: false,
  RETURN_DOM: false,
  RETURN_DOM_FRAGMENT: false,
  SANITIZE_DOM: true,
  KEEP_CONTENT: true,
  IN_PLACE: true,
  ALLOW_UNKNOWN_PROTOCOLS: false,
  USE_PROFILES: {
    html: true,
    svg: false,
    svgFilters: false,
    mathMl: false
  }
}

// 初始化 DOMPurify
let purify = DOMPurify

// 服务器端渲染 (SSR) 支持
if (typeof window === 'undefined') {
  const { JSDOM } = require('jsdom')
  const dom = new JSDOM('<!DOCTYPE html>')
  purify = DOMPurify(dom.window)
}

// 添加钩子
purify.addHook('uponSanitizeElement', hooks.uponSanitizeElement)
purify.addHook('uponSanitizeAttribute', hooks.uponSanitizeAttribute)

/**
 * 安全清理 HTML 内容
 * @param {string} dirty - 需要清理的 HTML 字符串
 * @param {Object} [customConfig] - 自定义配置（可选）
 * @returns {string} 安全的 HTML 字符串
 */
export function sanitizeHtml(dirty, customConfig = {}) {
  if (typeof dirty !== 'string' || !dirty.trim()) {
    return ''
  }

  // 合并配置
  const config = { ...defaultConfig, ...customConfig }

  // 清理 HTML
  return purify.sanitize(dirty, config)
}

/**
 * 安全清理 HTML 并返回 DOM 节点
 * @param {string} dirty - 需要清理的 HTML 字符串
 * @param {Object} [customConfig] - 自定义配置（可选）
 * @returns {DocumentFragment} 安全的 DOM 片段
 */
export function sanitizeToDom(dirty, customConfig = {}) {
  if (typeof dirty !== 'string' || !dirty.trim()) {
    return document.createDocumentFragment()
  }

  // 合并配置
  const config = {
    ...defaultConfig,
    ...customConfig,
    RETURN_DOM_FRAGMENT: true,
    RETURN_DOM: false
  }

  // 清理 HTML 并返回 DOM 片段
  return purify.sanitize(dirty, config)
}

/**
 * 安全清理 HTML 并返回纯文本
 * @param {string} dirty - 需要清理的 HTML 字符串
 * @returns {string} 纯文本内容
 */
export function sanitizeToText(dirty) {
  if (typeof dirty !== 'string' || !dirty.trim()) {
    return ''
  }

  // 先清理 HTML
  const cleanHtml = sanitizeHtml(dirty)

  // 创建临时元素获取文本内容
  const temp = document.createElement('div')
  temp.innerHTML = cleanHtml
  return temp.textContent || temp.innerText || ''
}

/**
 * 验证 URL 是否安全
 * @param {string} url - 需要验证的 URL
 * @returns {boolean} 是否安全
 */
export function isSafeUrl(url) {
  if (typeof url !== 'string') return false

  const safeProtocols = ['http:', 'https:', 'mailto:', 'tel:', 'ftp:']
  try {
    const parsed = new URL(url)
    return safeProtocols.includes(parsed.protocol)
  } catch (e) {
    return false
  }
}

/**
 * 清理用户输入（防止 XSS）
 * @param {string} input - 用户输入
 * @returns {string} 安全的文本
 */
export function sanitizeInput(input) {
  if (typeof input !== 'string') return ''

  // 移除 HTML 标签
  return input.replace(/<[^>]*>/g, '')
}
