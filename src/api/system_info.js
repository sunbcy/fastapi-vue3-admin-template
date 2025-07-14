import { request } from '@/utils/request'

// 搜索URL
export async function get_system_info() {
  return request({
    url: '/system_info/',
    method: 'get'
  })
}

export async function get_lan_info() {
  return request({
    url: '/system_info/get_lan_info',
    method: 'get'
  })
}

// 更新设备名称
export async function update_device_name(data) {
  return request({
    url: '/system_info/updateName',
    method: 'post',
    data
  })
}

export async function get_db_info() {
  return request({
    url: '/databases/get_db_info',
    method: 'get'
  })
}

export async function switch_db(data) {
  return request({
    url: '/databases/switch_db',
    method: 'post',
    data
  })
}

export async function switch_proxy_pool(data) {
  return request({
    url: '/spider_proxy_pool/proxy_pool',
    method: 'post',
    data
  })
}

export async function get_db_tables(data) {
  return request({
    url: '/databases/get_db_tables',
    method: 'post',
    data
  })
}

export async function get_databases() {
  return request({
    url: '/databases/get_databases',
    method: 'get'
  })
}

export async function update_project() {
  return request({
    url: '/system_info/update_project',
    method: 'get'
  })
}

export async function compile_project() {
  return request({
    url: '/system_info/compile_project',
    method: 'get'
  })
}

export async function restart_project() {
  return request({
    url: '/system_info/restart_project',
    method: 'get'
  })
}

export async function one_click_restart() {
  return request({
    url: '/system_info/one_click_restart',
    method: 'get'
  })
}
