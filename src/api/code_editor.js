import { request } from '@/utils/request'

export async function save_code(data) {
  return await request({
    url: '/code_editor/save_code',
    method: 'post',
    data
  })
}
