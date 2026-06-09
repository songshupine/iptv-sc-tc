from fastapi import FastAPI, Request, Query
from fastapi.responses import Response
import httpx

app = FastAPI()

FILE_MAP = {
    "ct": "ct.m3u8",
    "cmcc": "cmcc.m3u8",
    "cu": "cu.m3u8",
}

DEFAULT_IP = "192.168.100.1:4022"
BASE_URL = "https://tv.gotonas.com"  # ✅ 保持硬编码

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

    m3u8_url = f"{BASE_URL}/home/{FILE_MAP[file]}"

    try:
        # ✅ 增加 try-except 捕获网络异常
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            resp = await client.get(m3u8_url)
            resp.raise_for_status()  # 非 2xx 会抛异常
            m3u_text = resp.text
    except Exception as e:
        # ✅ 返回可读的错误信息，方便调试
        return Response(
            f"拉取 m3u8 失败: {m3u8_url}\n错误: {str(e)}",
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
        m3u_text = "\n".join(lines)  # ✅ 修复换行符

    return Response(
        content=m3u_text,
        media_type="application/vnd.apple.mpegurl",  # ✅ 修复换行符
        headers={
            "Cache-Control": "no-cache",
            "Access-Control-Allow-Origin": "*",
        },
    )
