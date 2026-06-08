from fastapi import FastAPI, Request
from fastapi.responses import Response
import os
import re

# 关闭 FastAPI 的自动斜杠重定向，防止 307 错误
app = FastAPI(redirect_slashes=False)

DEFAULT_IP = "192.168.100.1:4022"

FILE_MAP = {
    "udpxy": "udpxy_iptv.m3u8",
    "udpxy_cmcc": "udpxy_cmcc_iptv.m3u8",
    "udpxy_cun": "udpxy_cun_iptv.m3u8",
}

# 【关键】使用 {full_path:path} 接收 Next.js 透传过来的所有路径
@app.get("/{full_path:path}")
async def proxy_m3u8(
    request: Request,
    full_path: str,  # 例如: udpxy/192.168.2.30:8888
    aptv: str = None,
    fcc: str = None,
    r2h_token: str = None,
    rtspProxy: str = None,
    httpProxy: str = None  # 接收用户传入的 httpProxy 参数
):
    # 1. 手动解析路径，提取 rule_name 和 domain
    # full_path 格式为: "udpxy/192.168.2.30:8888"
    path_parts = full_path.split("/")
    if len(path_parts) < 2:
        return Response(content="Invalid path format. Expected: /udpxy/IP:PORT", status_code=400)
        
    rule_name = path_parts
    domain = path_parts
    path = "/".join(path_parts[2:]) if len(path_parts) > 2 else ""[[source_group_web_1]]

    # 2. 匹配对应的 m3u8 文件
    file_name = FILE_MAP.get(rule_name)
    if not file_name:
        return Response(content="Unknown route", status_code=404)

    # 3. 读取 m3u8 文件
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "..", "home", file_name)
    
    try:
        if not os.path.exists(file_path):
            return Response(content=f"File not found: {file_name}", status_code=404)
        with open(file_path, "r", encoding="utf-8") as f:
            m3u_text = f.read()
    except Exception as e:
        return Response(content=f"Error reading file: {str(e)}", status_code=500)

    # 4. aptv 替换
    if aptv is not None:
        m3u_text = m3u_text.replace(
            "{utc:YmdHMS}-{utcend:YmdHMS}", 
            "${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}"
        )

    # 5. IP 替换
    m3u_text = m3u_text.replace(DEFAULT_IP, domain)

    # 6. fcc 和 r2h-token 追加
    if fcc or r2h_token:
        lines = m3u_text.split("\n")
        for i, line in enumerate(lines):
            if "/udp/" in line:
                if "?" in line:
                    if fcc: lines[i] += f"&fcc={fcc}"
                    if r2h_token: lines[i] += f"&r2h-token={r2h_token}"
                else:
                    params = []
                    if fcc: params.append(f"fcc={fcc}")
                    if r2h_token: params.append(f"r2h-token={r2h_token}")
                    lines[i] += "?" + "&".join(params)
        m3u_text = "\n".join(lines)

    # 7. RTSP 代理替换
    if rtspProxy:
        if not rtspProxy.startswith("http"):
            rtspProxy = f"http://{rtspProxy}"
            
        lines = m3u_text.split("\n")
        for i, line in enumerate(lines):
            if 'catchup-source="rtsp://' in line:
                lines[i] = line.replace(
                    'catchup-source="rtsp://', 
                    f'catchup-source="{rtspProxy}/rtsp/'
                )
                if r2h_token:
                    lines[i] = re.sub(
                        r'(playseek=[^"&]*)', 
                        rf'\1&r2h-token={r2h_token}', 
                        lines[i]
                    )
        m3u_text = "\n".join(lines)

    # 8. 返回处理后的 m3u8 文件
    return Response(content=m3u_text, media_type="application/vnd.apple.mpegurl")
