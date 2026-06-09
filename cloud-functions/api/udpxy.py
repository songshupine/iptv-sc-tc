from fastapi import FastAPI, Request, Query
from fastapi.responses import Response
from functools import lru_cache
import httpx
import time

app = FastAPI()

# ===============================
# ✅ 三个 JS 的替换逻辑统一配置
# ===============================
FILE_CONFIG = {
    "ct": {"m3u8": "ct.m3u8", "time_sep": "-", "catchup_proto": "rtsp"},
    "cmcc": {"m3u8": "cmcc.m3u8", "time_sep": "/", "catchup_proto": "http"},
    "cu": {"m3u8": "cu.m3u8", "time_sep": "-", "catchup_proto": "rtsp"},
}

DEFAULT_IP = "192.168.100.1:4022"
BASE_URL = "https://tv.gotonas.com"
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

@app.get("/")
async def udpxy_proxy(
    request: Request,
    file: str = Query(...),
    ip: str = Query(DEFAULT_IP),
    aptv: str = Query(None),
    fcc: str = Query(None),
    rtspProxy: str = Query(None),
    httpProxy: str = Query(None),
):
    if file not in FILE_CONFIG:
        return Response("file 必须为 ct / cmcc / cu", status_code=400)

    cfg = FILE_CONFIG[file]

    try:
        # 1️⃣ 从缓存或源站获取 m3u8
        m3u_text = await fetch_m3u8_content(cfg)
    except Exception as e:
        return Response(f"m3u8 拉取失败: {e}", status_code=502)

    # 2️⃣ IP 替换
    m3u_text = m3u_text.replace(DEFAULT_IP, ip)

    # 3️⃣ APTV 时间占位符
    if aptv:
        m3u_text = m3u_text.replace(
            "{utc:YmdHMS}",
            "${(b)yyyyMMddHHmmss}",
        ).replace(
            "{utcend:YmdHMS}",
            "${(e)yyyyMMddHHmmss}",
        ).replace(
            "-" if cfg["time_sep"] == "-" else "/",
            cfg["time_sep"],
        )

    # 4️⃣ FCC 追加
    if fcc:
        lines = m3u_text.splitlines()
        for i, line in enumerate(lines):
            if "/udp/" in line:
                sep = "&" if "?" in line else "?"
                lines[i] += f"{sep}fcc={fcc}"
        m3u_text = "\n".join(lines)

    # 5️⃣ Catchup Proxy
    proxy = httpProxy if httpProxy else rtspProxy
    if proxy:
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
