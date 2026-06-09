from fastapi import FastAPI, Request, Query, status
from fastapi.responses import Response, RedirectResponse
from functools import lru_cache
import httpx
import time

app = FastAPI()

# ===============================
# ✅ 修复 1：BASE_URL 必须填写
# ===============================
BASE_URL = "https://tv.gotonas.com"

# ===============================
# ✅ 三个 JS 的替换逻辑统一配置
# ===============================
FILE_CONFIG = {
    "ct": {"m3u8": "ct.m3u8", "time_sep": "-", "catchup_proto": "rtsp"},
    "cmcc": {"m3u8": "cmcc.m3u8", "time_sep": "/", "catchup_proto": "http"},
    "cu": {"m3u8": "cu.m3u8", "time_sep": "-", "catchup_proto": "rtsp"},
}

DEFAULT_IP = "192.168.100.1:4022"
CACHE_TTL = 10  # 缓存 10 秒

# ===============================
# ✅ 带 TTL 的内存缓存装饰器
# ===============================
def ttl_cache(maxsize=128, ttl=CACHE_TTL):
    def decorator(func):
        cache = {}
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache:
                value, timestamp = cache[key]
                if now - timestamp < ttl:
                    return value
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

@ttl_cache(ttl=CACHE_TTL)
async def fetch_m3u8_content(file_cfg: dict):
    """带缓存的 m3u8 拉取函数"""
    async with httpx.AsyncClient(timeout=5, follow_redirects=True) as client:
        resp = await client.get(f"{BASE_URL}/home/{file_cfg['m3u8']}")
        resp.raise_for_status()
        return resp.text

@app.get("/{full_path:path}")
async def udpxy_proxy(
    request: Request,
    full_path: str,
    file: str = Query(...),
    ip: str = Query(DEFAULT_IP),
    aptv: str = Query(None),
    fcc: str = Query(None),
    rtspProxy: str = Query(None),
    httpProxy: str = Query(None),
):
    # ✅ 修复 3：处理尾部斜杠
    if full_path and full_path.endswith("/"):
        return RedirectResponse(
            url=str(request.url).rstrip("/"),
            status_code=status.HTTP_301_MOVED_PERMANENTLY,
        )

    if file not in FILE_CONFIG:
        return Response("file 必须为 ct / cmcc / cu", status_code=400)

    cfg = FILE_CONFIG[file]

    try:
        m3u_text = await fetch_m3u8_content(cfg)
    except Exception as e:
        return Response(f"m3u8 拉取失败: {e}", status_code=502)

    # IP 替换
    m3u_text = m3u_text.replace(DEFAULT_IP, ip)

    # APTV 时间占位符
    if aptv:
        m3u_text = (
            m3u_text.replace("{utc:YmdHMS}", "${(b)yyyyMMddHHmmss}")
            .replace("{utcend:YmdHMS}", "${(e)yyyyMMddHHmmss}")
            .replace("-" if cfg["time_sep"] == "-" else "/", cfg["time_sep"])
        )

    # FCC 追加
    if fcc:
        lines = m3u_text.splitlines()
        for i, line in enumerate(lines):
            if "/udp/" in line:
                sep = "&" if "?" in line else "?"
                lines[i] += f"{sep}fcc={fcc}"
        m3u_text = "\n".join(lines)

    # Catchup Proxy
    proxy = httpProxy if httpProxy else rtspProxy
    if proxy:
        # ✅ 修复 2：确保代理地址有 http 协议头
        if not proxy.startswith("http"):
            proxy = f"http://{proxy}"
        
        proto = cfg["catchup_proto"]
        lines = m3u_text.splitlines()
        for i, line in enumerate(lines):
            if f'catchup-source="{proto}://' in line:
                lines[i] = line.replace(
                    f'catchup-source="{proto}://',
                    f'catchup-source="{proxy}/{proto}/',
                )
        m3u_text = "\n".join(lines)

    return Response(
        content=m3u_text,
        media_type="application/vnd.apple.mpegurl",
        headers={"Cache-Control": "no-cache", "Access-Control-Allow-Origin": "*"},
    )
