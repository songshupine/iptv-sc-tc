# 🎬 四川 电信 移动 联通 IPTV 直播源

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> 📺 **IPTV 机顶盒替代方案** | 支持回看、时移 | 每周不定时更新  
> 📅 **更新时间**：2026-06-12 14:29:12 | 共 **150** 条频道信息

---
> 此项目基于 [suzukua/iptv-cd-telecom](https://github.com/suzukua/iptv-cd-telecom) 开发
---
> 部署在腾讯 EdgeOne Pages 上，国内访问更快更稳定，注意部分参数使用方法和原项目有差异
---

## ✨ 核心特性

- 🎬 **广泛兼容**：支持 tvbox、KODI、fileball、APTV、mytv-android 等主流播放器
- 🔄 **回看时移**：支持节目回看和时移功能，不错过精彩内容（**仅电信和部分移动**）
- 📡 **灵活接入**：提供官方单播源、组播转单播（udpxy / msd_lite / rtp2httpd）多种方式
- 🎯 **4K 超清**：已解决部分 4K 频道播放问题，享受超高清画质
- 📺 **完整节目单**：每天多次更新 EPG，覆盖央视、卫视超 100 套频道

---

## 📖 使用指南

### 🚀 方式一：官方组播 / 单播源

直接复制以下地址到播放器即可使用，无需额外配置：

**电信组播标准版：**

https://tv.gotonas.com/home/iptv.m3u8


**电信组播 APTV 兼容版：**

https://tv.gotonas.com/home/apt_iptv.m3u8


**联通单播版：**

https://tv.gotonas.com/home/cun_iptv.m3u8


> 💡 **提示**：两个版本电信都支持时移功能，APTV 版针对时区兼容性进行了优化

---

### 🔧 方式二：组播转单播（推荐）

适用于已搭建 udpxy、msd_lite、rtp2httpd 等工具的用户。

#### 📌 格式说明

https://tv.gotonas.com/api/udp?file=ct&[host:port]&[其他参数]


#### 🎯 使用示例

**基础用法：**

https://tv.gotonas.com/api/udp?file=ct&ip=192.168.2.30:8888


**APTV + FCC + RTSP 代理（复杂示例）：**

https://tv.gotonas.com/api/udp?file=ct&ip=192.168.2.30:8888&aptv=1&fcc=183.223.164.65:8027&rtspProxy=192.168.2.30:8888


**回放转单播 (RTSP → HTTP)：**

https://tv.gotonas.com/api/udp?file=ct&ip=192.168.100.1:4022


**排除4K和专区频道（示例）：**

https://tv.gotonas.com/api/udp?file=ct&ip=192.168.2.30:8888&filter=4K,专区


**组合使用过滤和其他参数：**

https://tv.gotonas.com/api/udp?file=ct&ip=192.168.2.30:8888&aptv=1&fcc=183.223.164.65:8027&filter=4K


#### 📋 参数说明

| 参数 | 功能描述 | 使用示例 | 适用场景 |
|------|----------|----------|----------|
| `file=ct` | 使用的运营商文件 | `file=ct` | `ct` `cu` `cmcc` 分别对应电信/联通/移动 |
| `ip=host:port` | udpxy 代理地址和端口 | `ip=192.168.1.1:8888` | udpxy 代理服务器地址，可以是 `http` 或者 `https` 开头 |
| `aptv=1` | 启用 APTV +8 时区兼容 | `aptv=1` | APTV、mytv-android 等播放器 |
| `fcc=host:port` | 启用 FCC 快速换台模式 | `fcc=182.139.234.40:8027` | 需要快速切换频道的场景 |
| `rtspProxy=host:port` | RTSP 转 HTTP 播放 | `rtspProxy=192.168.100.2:4022` | 不支持 RTSP 协议的播放器 / 外网回看时代理 |
| `r2h-token=token` | r2h-token 参数 | `r2h-token=mytoken` | 有 r2h-token 时使用 |
| `httpProxy=host:port` | http 代理播放 | `httpProxy=192.168.100.2:4022` | 外网回看（联通），可以加 `http` 或者 `https` |
| `txt=1` | 控制 txt 头返回，默认 txt | `txt=0` | `1` 可以让播放器接收到 `u3u8` 头 |

> 📝 **说明**：
> - 回看时间参数格式：`playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}`
> - **电信 FCC 服务器**：`182.139.234.40:8027`
> - **移动 FCC 服务器**：`183.223.164.65:8027`
> - `rtspProxy` 支持 HTTP/HTTPS 协议，可指定 `rtspProxy=https://192.168.100.2:4022` (电信回看使用)
> - `httpProxy` 支持 HTTP/HTTPS 协议，可指定 `httpProxy=https://192.168.100.2:4022` (联通回看使用，需要较新的 rtp2httpd)

---

## 📺 EPG 电子节目单

每天自动同步原项目多次到国内服务器，覆盖 **央视、卫视超 100 套频道**：

https://epg.gotonas.com/t.xml.gz


> 🔄 **更新频率**：每天多次自动更新，确保节目单准确性

---

## 💬 问题反馈

遇到问题或有建议？欢迎通过以下方式反馈：

- 📮 **提交 Issue**：[GitHub Issues](https://github.com/songshupine/iptv-sc-tc/issues)
- 💡 **功能建议**：欢迎在 Issues 中提出你的想法

> 🙏 **提示**：提交问题时请详细描述你的使用场景和遇到的错误信息

---

## 📝 免责声明

- ⚖️ 本项目仅供 **学习交流** 使用
- 🔒 请在 **合法合规** 的范围内使用本项目提供的服务
- 📌 本项目不提供任何视频内容，所有内容来源于公开的 IPTV 服务
