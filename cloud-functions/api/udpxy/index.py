# cloud-functions/udpxy/index.py
from fastapi import FastAPI
from fastapi.responses import Response
import os
import re

app = FastAPI()

# 默认需要被替换的 IP 地址
DEFAULT_IP = "192.168.100.1:4022"

# 定义路径前缀与 home 目录下 m3u8 文件的映射关系
FILE_MAP = {
    "udpxy": "udpxy_iptv.m3u8",
    "udpxy_cmcc": "udpxy_cmcc_iptv.m3u8",
    "udpxy_cun": "udpxy_cun_iptv.m3u8",
}

@app.get("/{rule_name}/{domain}/{path:path}")
async def proxy_m3u8(
    rule_name: str, 
    domain: str, 
    path: str = "",
    aptv: str = None,
    fcc: str = None,
    r2h_token: str = None,
    rtspProxy: str = None
):
    # 1. 检查文件映射是否存在
    file_name = FILE_MAP.get(rule_name)
    if not file_name:
        return Response(content=f"Unknown route: {rule_name}", status_code=404)

    # 2. 读取 home 目录下的 m3u8 文件
    file_path = os.path.join("home", file_name)
    try:
        if not os.path.exists(file_path):
            return Response(content=f"File not found: {file_name}", status_code=404)
        with open(file_path, "r", encoding="utf-8") as f:
            m3u_text = f.read()
    except Exception as e:
        return Response(content=f"Error reading file: {str(e)}", status_code=500)

    # 3. aptv 参数处理：替换时间占位符
    if aptv is not None:
        m3u_text = m3u_text.replace(
            "{utc:YmdHMS}-{utcend:YmdHMS}", 
            "${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}"
        )

    # 4. IP 替换：将默认 IP 替换为 URL 中传入的 domain
    m3u_text = m3u_text.replace(DEFAULT_IP, domain)

    # 5. 逐行处理 fcc 和 r2h-token 参数追加
    if fcc or r2h_token:
        lines = m3u_text.split("\n")
        for i, line in enumerate(lines):
            if "/udp/" in line:
                # 判断当前行是否已有查询参数
                if "?" in line:
                    if fcc: lines[i] += f"&fcc={fcc}"
                    if r2h_token: lines[i] += f"&r2h-token={r2h_token}"
                else:
                    params = []
                    if fcc: params.append(f"fcc={fcc}")
                    if r2h_token: params.append(f"r2h-token={r2h_token}")
                    lines[i] += "?" + "&".join(params)
        m3u_text = "\n".join(lines)

    # 6. RTSP 代理替换
    if rtspProxy:
        # 确保 rtspProxy 带有 http 前缀
        if not rtspProxy.startswith("http"):
            rtspProxy = f"http://{rtspProxy}"
            
        lines = m3u_text.split("\n")
        for i, line in enumerate(lines):
            if 'catchup-source="rtsp://' in line:
                # 替换 rtsp 协议前缀
                lines[i] = line.replace(
                    'catchup-source="rtsp://', 
                    f'catchup-source="{rtspProxy}/rtsp/'
                )
                # 如果同时传了 r2h-token，处理 playseek 参数
                if r2h_token:
                    lines[i] = re.sub(
                        r'(playseek=[^"&]*)', 
                        rf'\1&r2h-token={r2h_token}', 
                        lines[i]
                    )
        m3u_text = "\n".join(lines)

    # 7. 返回处理后的 m3u8 文件
    return Response(content=m3u_text, media_type="application/vnd.apple.mpegurl")
