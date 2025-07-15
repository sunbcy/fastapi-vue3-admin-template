import { request } from '@/utils/request'

// 搜索URL
export async function get_block_info() {
  return await request({
    url: '/jiucaigongshe/',
    method: 'get'
  })
}
