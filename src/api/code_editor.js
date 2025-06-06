import { request } from '@/utils/request'

export function save_code(data) {
  return request({
    url: '/code_editor/save_code',
    method: 'post',
    data
  })
}
