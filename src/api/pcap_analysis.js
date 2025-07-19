import { request } from '@/utils/request'

// 传递名单
export async function get_analysis_info(data) {
  return await request({
    url: '/pcap_analysis/analysis',
    method: 'post',
    data
  })
}
