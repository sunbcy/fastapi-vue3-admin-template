<p align="center">
  <strong>fastapi-vue3-admin-template</strong>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/python-3.10.0-brightgreen.svg" >
    <img src="https://img.shields.io/badge/fastapi-0.115.4-brightgreen.svg" >
    <img src="https://img.shields.io/badge/vue-3.3.4-brightgreen.svg" >
    <img src="https://img.shields.io/badge/element--plus-2.3.12-brightgreen.svg" >
    <img src="https://img.shields.io/badge/vue--router-4.2.4-brightgreen.svg" >
    <img src="https://img.shields.io/badge/pinia-2.1.6-brightgreen.svg" >
    <img src="https://img.shields.io/badge/vite-5.0.0-brightgreen.svg" >
</p>

# fastapi-vue3-admin-template

一个基于 **FastAPI + Vue3 + Element Plus** 的全栈中后台模板。它不止是通用管理后台脚手架，还内置了多个真实业务模块：**网页数据采集（韭研公社 / 猎聘 / 每日格言）、网络数据包（pcap）分析、基于机器学习的网页分类、以及主机/系统信息管理**。

> 定位：在通用 admin 模板（动态路由、权限、多布局、国际化）基础上，集成了若干"数据采集 + 分析"工具型模块，适合作为爬虫/网络安全/数据分析类项目的二次开发基础。

---

## 项目架构

```
┌─────────────────┐         /api 代理 (vite)          ┌──────────────────────┐
│   Vue3 前端      │  ──────────────────────────────▶  │   FastAPI 后端        │
│  (port 5173)     │   http://192.168.124.4:5055       │   (port 5055)         │
│  Element Plus    │                                    │   uvicorn + uvloop    │
└─────────────────┘                                    └──────────────────────┘
        │                                                          │
        │  npm run build:prod → dist/                             │ 挂载 dist/ 静态资源
        └────────────────────────────────────────────────────────┘
```

- **前端**：Vite + Vue3 + Vue Router + Pinia + Element Plus，开发服务器 5173，生产构建输出到 `dist/`，由后端直接托管。
- **后端**：FastAPI 应用，监听 `0.0.0.0:5055`，MacOS 下使用 `uvloop` 事件循环；通过 `main.py` 的 `/` 路由返回 `dist/index.html`，并把 `/assets` 挂载为静态目录，**前后端同端口部署**。
- **配置**：`config.yaml` 按 `Android / MacOS / Windows` 三平台分别定义 MySQL、Redis、Elasticsearch、下载路径、server 地址等。

---

## 功能模块

### 通用后台能力

- 登录 / 注销
- 动态路由 + 权限验证（页面权限、指令权限、按钮权限）
- 多布局（default / classic / streamline）、动态换肤、国际化多语言
- 动态侧边栏、面包屑、标签页（tags-view）、Svg 图标、全屏

### 业务模块一览

| 模块       | 前端路由                     | 后端前缀                 | 功能说明                                                                           |
| ---------- | ---------------------------- | ------------------------ | ---------------------------------------------------------------------------------- |
| Dashboard  | `/dashboard`                 | —                        | 概览首页                                                                           |
| 代码编辑器 | `/code_editor`               | `/api/code_editor`       | 在线编辑并保存代码到服务端 `CodeRepo/`                                             |
| 韭研公社   | `/big_a_stock/jiucaigongshe` | `/api/jiucaigongshe`     | 采集韭研公社（九阳公社）A 股异动分析数据，含 API token 签名（execjs）              |
| 猎聘网     | `/liepin`                    | `/api/liepin`            | 搜索猎聘职位 + 抓取职位详情（公司/薪资/要求/简介）                                 |
| 每日格言   | （Dashboard 展示）           | `/api/azquotes`          | 异步爬虫抓取 azquotes 当日名言                                                     |
| 数据包分析 | `/pcap_analysis`             | `/api/pcap_analysis`     | 上传 pcap/pcapng，统计协议分布、LAN/WAN IP、主机 IP（scapy + 线程池 + SSE 进度流） |
| ECharts    | `/echarts`                   | —                        | 图表展示示例                                                                       |
| 网页分类   | `/webclassification`         | `/api/webclassification` | 网页预处理 → 特征抽取 → 特征选择 → 朴素贝叶斯分类（sklearn + jieba + nltk）        |
| 系统管理   | `/menu` `/role` `/user`      | `/api/system`            | 菜单/角色/用户管理（模板示例）                                                     |
| 系统信息   | （系统管理内）               | `/api/system_info`       | 采集 CPU/磁盘/内外网 IP/地理位置、LAN 设备扫描（nmap）、git 拉取/构建/重启项目     |

### 后端模块实现细节

**`app/azquotes`** — 每日格言爬虫

- `GET /api/azquotes/`：用 `aiohttp` + `lxml` 异步抓取 azquotes.com 当日名言，支持代理（`utils.check_proxy`）。

**`app/jiucaigongshe`** — 韭研公社 A 股异动

- `GET /api/jiucaigongshe/`：调用韭研公社 App API（带 `execjs` 计算 `token` 签名 + 固定 cookie），获取当日/前一交易日异动板块数据；缺数据自动回退到历史日期。

**`app/liepin`** — 猎聘职位采集

- `POST /api/liepin/get_jobs`：按城市/关键词/经验/页码搜索职位，自动翻页聚合。
- `POST /api/liepin/getJobDetails`：抓取单个职位详情（JD、公司信息、融资阶段等）。
- `GET /api/liepin/get_top_ten_industries`：行业 Top10 统计（数据库或内置默认值）。

**`app/code_editor`** — 在线代码保存

- `POST /api/code_editor/save_code`：用 `aiofiles` 异步写入 `CodeRepo/<filename>`。

**`app/pcap_analysis`** — 数据包分析

- `POST /api/pcap_analysis/upload`：上传 pcap/pcapng 到 `uploads/`。
- `POST /api/pcap_analysis/analysis`：为每个文件创建后台分析任务（线程池 `ThreadPoolExecutor` 跑 `scapy.rdpcap`）。
- `GET /api/pcap_analysis/task/status/{id}`、`/task/result/{id}`：查询任务状态与结果。
- `GET /api/pcap_analysis/stream-progress/{id}`：SSE 实时进度推送。
- 分析结果：主机 IP、`protocol_types`（IP/TCP/UDP/DNS/HTTP/HTTPS/… 计数）、LAN/WAN IP 划分。

**`app/webclassification`** — 网页分类（ML 流水线）

- `POST /api/webclassification/process`：对给定 URL 执行四步流水线：
  1. `preprocess`：requests 抓取 → BeautifulSoup 解析 → jieba + nltk 中英分词 → 停用词过滤 → 词干提取（`app/webclassification/modules/preprocess.py`）
  2. `feature_extract`：构造特征（`feature_extract.py`）
  3. `feature_select`：文档频率过滤（`feature_select.py`）
  4. `classify`：TfidfVectorizer + 自定义 DFSelector + MultinomialNB 朴素贝叶斯分类（`classify.py`，`train_model` 可持久化 joblib 模型）
- ⚠️ 此模块强依赖 `scipy`（sklearn 底层）。在 macOS 27.0 上 PyPI 预编译 wheel 有 dyld 段格式缺陷，需本地源码重装：`pip install --no-binary scipy --force-reinstall scipy`（需先 `brew install openblas` 与 gfortran）。

**`app/system`** — 系统管理（模板示例）

- `POST /api/system/login`：示例登录接口（返回 ok）。菜单/角色/用户前端页面为 admin 模板脚手架。

**`app/system_info`** — 主机与系统信息

- `GET /api/system_info/`：CPU、磁盘、内外网 IP、地理定位（ipinfo.io）、cip.cc IP 查询。
- `GET /api/system_info/get_lan_info`：局域网设备扫描（MacOS 用 `sudo` 跑 `scan_network.py` 获取 IP/MAC；Android 用 `nmap`）。
- `GET /api/system_info/update_project`：`git pull` 更新仓库。
- `GET /api/system_info/compile_project`：执行 `npm run build:prod` 重新构建前端。
- `GET /api/system_info/restart_project`：按端口查找并重启后端进程。

---

## 目录结构

```
.
├── README.md
├── config.yaml                 # 多平台配置（MySQL/Redis/ES/下载路径/server）
├── init_project.py             # 初始化脚本（依据平台生成配置）
├── deploy.sh                   # 部署脚本
├── mac_start.sh / win_start.bat / termux_start.sh   # 各平台启动脚本
├── index.html
├── vite.config.js              # Vite 配置 + /api 代理（指向后端 HTTP 地址）
├── api/                        # FastAPI 后端
│   ├── main.py                 # 入口，托管 dist 静态资源
│   ├── app/
│   │   ├── __init__.py         # create_app / register_routers
│   │   ├── azquotes/           # 每日格言爬虫
│   │   ├── jiucaigongshe/      # 韭研公社 A股异动
│   │   ├── liepin/             # 猎聘职位采集
│   │   ├── code_editor/        # 在线代码保存
│   │   ├── pcap_analysis/      # 数据包分析
│   │   ├── webclassification/  # 网页分类（ML）
│   │   ├── system/             # 系统管理示例
│   │   ├── system_info/        # 主机/系统信息
│   │   └── utils/              # 响应封装、代理检测、IP/OS 工具、pcap 工具
│   ├── venv_mac_310/           # macOS Python 3.10 虚拟环境（本机使用）
│   └── requirements_mac.txt / requirements_win.txt / requirements_termux.txt
├── src/                        # Vue3 前端
│   ├── api/                    # 各模块 axios 封装
│   ├── views/                  # 页面（含各业务模块）
│   ├── router/                 # 路由（constantRoutes + asyncRoutes）
│   ├── store/                  # Pinia（user/permission/settings/tagsView...）
│   ├── layout/                 # 多布局
│   └── utils/                  # request 封装、storage、security 等
└── public/
```

---

## 环境要求

- **前端**：Node.js ≥ 18（推荐 pnpm）
- **后端**：Python ≥ 3.10（本机使用 `api/venv_mac_310`，即 Python 3.10.17）
- **部分模块额外依赖**：
  - 网页分类：`scipy`（见上方 macOS 27.0 重装说明）
  - 数据包分析：`scapy`
  - 系统信息局域网扫描：MacOS 需 `sudo` 权限；Android 需 `nmap`
  - 韭研公社：依赖 `api/api_js/jiuyangongshe_api.js`（execjs 签名）

---

## 安装与运行

### 1. 前端依赖

```bash
pnpm install      # 或 yarn install（推荐 pnpm/yarn，避免 npm 诡异问题）
```

### 2. 后端依赖（使用虚拟环境）

```bash
cd api
source venv_mac_310/bin/activate        # macOS
pip install -r requirements_mac.txt     # 或 win / termux 对应文件
```

### 3. 初始化（可选）

```bash
python3 init_project.py     # 依据当前平台生成配置
```

### 4. 启动后端

```bash
cd api
source venv_mac_310/bin/activate
uvicorn main:app --host 0.0.0.0 --port 5055 --reload
# 或直接：
./mac_start.sh
```

### 5. 启动前端（开发模式）

```bash
pnpm dev        # 默认 http://localhost:5173
```

> ⚠️ **代理配置注意**：`vite.config.js` 中的 `/api` 代理必须指向 **后端真实 HTTP 地址**。本机后端在 `http://192.168.124.4:5055`（或 `http://127.0.0.1:5055`），务必使用 `http://` 而非 `https://`，否则前端请求会报 502。
>
> 若更换网络导致 IP 变化，请同步修改 `vite.config.js` 的 `target`。

### 6. 生产构建（前后端同端口）

```bash
pnpm build:prod          # 输出到 dist/
# 后端 main.py 已挂载 dist/，访问 http://<server>:5055 即可
```

---

## 其他

基于 [vue3-admin-template](https://github.com/zhihuifanqiechaodan/vue3-admin-template.git) 二次开发，集成了数据采集/网络安全/机器学习类业务模块。欢迎提 issues 或 PR。
