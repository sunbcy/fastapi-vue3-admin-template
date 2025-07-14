import { request } from '@/utils/request'

// 搜索URL
export async function getTodayQuote() {
  return request({
    url: '/azquotes',
    method: 'get'
  })
}
