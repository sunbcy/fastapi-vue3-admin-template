import { request } from '@/utils/request'

// 传递名单
export async function get_analysis_info(data) {
  return await request({
    url: '/pcap_analysis/analysis',
    method: 'post',
    data
  })
}

export async function upload_pcaps(data) {
  return await request({
    url: '/pcap_analysis/upload',
    method: 'post',
    data
  })
}
