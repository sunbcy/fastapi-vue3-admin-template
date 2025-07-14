import { request } from '@/utils/request'

export async function read_todos() {
  return request({
    url: '/todo/read_todos',
    method: 'get'
  })
}

export async function write_todos(data) {
  return request({
    url: '/todo/write_todos',
    method: 'post',
    data
  })
}

export async function edit_write_todos(data) {
  return request({
    url: '/todo/edit_write_todos',
    method: 'post',
    data
  })
}

export async function del_todos(data) {
  return request({
    url: '/todo/del_todos',
    method: 'post',
    data
  })
}
