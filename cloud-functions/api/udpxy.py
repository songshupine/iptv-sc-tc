from fastapi import FastAPI, Request, Query
from fastapi.responses import Response
import httpx

app = FastAPI()

# -----------------------------
# 不同 file 的映射配置
# -----------------------------
FILE_CONFIG = {
    "ct": {
        "m3u8": "ct.m3u8",
        "time_pattern": "{utc:YmdHMS}-{utcend:YmdHMS}",
        "time_replace": "${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}",
        "catchup_proto": "rtsp",
    },
    "cmcc": {
        "m3u8": "cmcc.m3u8",
        "time_pattern": "{utc:YmdHMS}/{utcend:YmdHMS}",
        "time_replace": "${(b)yyyyMMddHHmmss}/${(e)yyyyMMddHHmmss}",
        "catchup_proto": "http",
    },
    "cu": {
        "m3u8": "cu.m3u8",
        "time_pattern": "{utc:YmdHMS}-{utcend:YmdHMS}",
        "time_replace": "${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}",
        "catchup_proto": "rtsp",
    },
}

# ✅ 硬编码 BASE_URL
BASE_URL = "https://tv.gotonas.com"
DEFAULT_IP = "192.168.100.1:4022"


# ✅ 路由改为 @app.get("/")
@app.get("/")
async def udpxy_proxy(
    request: Request,
    file: str = Query(...),
    ip: str = Query(DEFAULT_IP),
    aptv: str = Query(None),
    fcc: str = Query(None),
    r2h_token: str = Query(None, alias="r2h-token"),
    httpProxy: str = Query(None),
    rtspProxy: str = Query(None),
):
    if file not in FILE_CONFIG:
        return Response("file 必须为 ct / cmcc / cu", status_code=400)

    cfg = FILE_CONFIG[file]

    # 1. 拉取对应 m3u8
    m3u_url = f"{BASE_URL}/home/{cfg['m3u8']}"
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        resp = await client.get(m3u_url)
        if resp.status_code != 200:
            return Response(
                f"m3u8 拉取失败: {m3u_url}",
                status_code=502,
            )
        m3u_text = resp.text

    # 2. IP 替换
    m3u_text = m3u_text.replace(DEFAULT_IP, ip)

    # 3. APTV 时间占位符
    if aptv:
        m3u_text = m3u_text.replace(
            cfg["time_pattern"],
            cfg["time_replace"],
        )

    # 4. fcc 追加
    if fcc:
        lines = m3u_text.splitlines()
        for i, line in enumerate(lines):
            if "/udp/" in line:
                sep = "&" if "?" in line else "?"
                lines[i] += f"{sep}fcc={fcc}"
        m3u_text = "\n".join(lines)

    # 5. r2h-token
    if r2h_token:
        lines = m3u_text.splitlines()
        for i, line in enumerate(lines):
            if "/udp/" in line or "playseek=" in line:
                sep = "&" if "?" in line else "?"
                lines[i] += f"{sep}r2h-token={r2h_token}"
        m3u_text = "\n".join(lines)

    # 6. catchup proxy（cmcc/http，ct&cu/rtsp）
    proxy = httpProxy if httpProxy else rtspProxy
    if proxy:
        if not proxy.startswith("http"):
            proxy = f"{proxy}"
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
        headers={
            "Cache-Control": "no-cache",
            "Access-Control-Allow-Origin": "*",
        },
    )
