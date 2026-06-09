from fastapi import FastAPI, Request, Query
from fastapi.responses import Response
import httpx

app = FastAPI()

# ===============================
# ✅ 三个 JS 的替换逻辑统一配置
# ===============================
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

DEFAULT_IP = "192.168.100.1:4022"
BASE_URL = "https://tv.gotonas.com"

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

    # 1️⃣ 拉取对应 m3u8
    m3u8_url = f"{BASE_URL}/home/{cfg['m3u8']}"
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        resp = await client.get(m3u8_url)
        if resp.status_code != 200:
            return Response(
                f"m3u8 文件不存在: {m3u8_url}",
                status_code=404,
            )
        m3u_text = resp.text

    # 2️⃣ IP 替换
    m3u_text = m3u_text.replace(DEFAULT_IP, ip)

    # 3️⃣ APTV 时间占位符（按 file 自动切换）
    if aptv:
        m3u_text = m3u_text.replace(
            cfg["time_pattern"],
            cfg["time_replace"],
        )

    # 4️⃣ FCC 追加
    if fcc:
        lines = m3u_text.splitlines()
        for i, line in enumerate(lines):
            if "/udp/" in line:
                sep = "&" if "?" in line else "?"
                lines[i] += f"{sep}fcc={fcc}"
        m3u_text = "\n".join(lines)

    # 5️⃣ catchup-source 代理（整合 3 个 JS）
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
        headers={
            "Cache-Control": "no-cache",
            "Access-Control-Allow-Origin": "*",
        },
    )
