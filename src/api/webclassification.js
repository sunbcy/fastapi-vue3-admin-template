import { request } from '@/utils/request'

export function get_process_result(data) {
  return request({
    url: '/webclassification/process',
    method: 'post',
    data
  })
}
