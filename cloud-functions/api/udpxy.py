from fastapi import FastAPI, Request, Query
from fastapi.responses import Response
import httpx
import os

app = FastAPI()

FILE_MAP = {
    "ct": "ct.m3u8",
    "cmcc": "cmcc.m3u8",
    "cu": "cu.m3u8",
}

DEFAULT_IP = "192.168.100.1:4022"
base_url = "https://tv.gotonas.com"  # ✅ 保持硬编码

@app.get("/{full_path:path}")
async def udpxy_proxy(
    request: Request,
    full_path: str,
    file: str = Query(...),
    ip: str = Query(DEFAULT_IP),
    aptv: str = Query(None),
    fcc: str = Query(None),
):
    if file not in FILE_MAP:
        return Response("file 必须为 ct / cmcc / cu", status_code=400)

    m3u8_url = f"{base_url}/home/{FILE_MAP[file]}"

    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            resp = await client.get(m3u8_url)
            resp.raise_for_status()
            m3u_text = resp.text
    except Exception as e:
        return Response(
            f"m3u8 拉取失败: {m3u8_url}\n{e}",
            status_code=502,
        )

    # IP 替换
    m3u_text = m3u_text.replace(DEFAULT_IP, ip)

    # aptv 时间占位符
    if aptv:
        m3u_text = m3u_text.replace(
            "{utc:YmdHMS}-{utcend:YmdHMS}",
            "${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}",
        )

    # fcc 追加
    if fcc:
        lines = m3u_text.splitlines()
        for i, line in enumerate(lines):
            if "/udp/" in line:
                sep = "&" if "?" in line else "?"
                lines[i] += f"{sep}fcc={fcc}"
        m3u_text = "\n".join(lines) 

    return Response(
        content=m3u_text,
        media_type="application/vnd.apple.mpegurl", 
        headers={
            "Cache-Control": "no-cache",
            "Access-Control-Allow-Origin": "*",
        },
    )
