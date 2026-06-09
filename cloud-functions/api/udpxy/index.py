from fastapi import FastAPI, Request, Query
from fastapi.responses import Response, JSONResponse
import os
import re

app = FastAPI()

# 默认需要被替换的 IP 地址
DEFAULT_IP = "192.168.100.1:4022"

# 定义文件映射关系
FILE_MAP = {
    "udpxy": "udpxy_iptv.m3u8",
    "udpxy_cmcc": "udpxy_cmcc_iptv.m3u8",
    "udpxy_cun": "udpxy_cun_iptv.m3u8",
}

# ==========================================
# 1. 新增：参数调试接口
# ==========================================
@app.get("/api/udpxy/debug")
async def debug_params(request: Request):
    """
    将收到的所有查询参数以 JSON 格式返回，方便前端调试
    """
    # 获取所有的查询参数（返回一个字典）
    all_params = dict(request.query_params)
    
    return JSONResponse(content={
        "message": "参数接收成功",
        "received_params": all_params
    })

# ==========================================
# 2. 原有的业务接口
# ==========================================
@app.get("/{full_path:path}")
async def proxy_m3u8(
    request: Request,
    file: str = Query(..., description="文件类型，如 udpxy, udpxy_cmcc"),
    ip: str = Query(..., description="替换后的目标 IP 和端口"),
    aptv: str = Query(None, description="aptv 参数"),
    fcc: str = Query(None, description="fcc 代理地址"),
    r2h_token: str = Query(None, description="r2h token"),
    rtspProxy: str = Query(None, description="RTSP 代理地址"),
    httpProxy: str = Query(None, description="HTTP 代理地址")
):
    # 1. 检查文件映射是否存在
    file_name = FILE_MAP.get(file)
    if not file_name:
        return Response(content=f"Unknown file type: {file}", status_code=404)

    # 2. 读取 m3u8 文件
    base = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base, "public", "home", file_name)
    try:
        if not os.path.exists(file_path):
            return Response(content=f"File not found: {file_path}", status_code=404)
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

    # 4. IP 替换：将默认 IP 替换为 URL 中传入的 ip 参数
    m3u_text = m3u_text.replace(DEFAULT_IP, ip)

    # 5. 逐行处理 fcc 和 r2h-token 参数追加
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

    # 6. RTSP 代理替换
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

    # 7. 返回处理后的 m3u8 文件
    return Response(content=m3u_text, media_type="application/vnd.apple.mpegurl")
