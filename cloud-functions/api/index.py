from fastapi import FastAPI, Request, Query
from fastapi.responses import Response
import httpx

app = FastAPI()

FILE_MAP = {
    "ct": "udpxy_iptv.m3u8",
    "cmcc": "cmcc.m3u8",
    "cu": "cu.m3u8",
}

DEFAULT_IP = "192.168.100.1:4022"

def get_base_url(request: Request) -> str:
    scheme = request.headers.get("x-forwarded-proto", "https")
    host = request.headers.get("x-forwarded-host") or request.headers.get("host")
    return f"{scheme}://{host}"

@app.get("/udpxy/")
async def udpxy_proxy(
    request: Request,
    file: str = Query(...),
    ip: str = Query(DEFAULT_IP),
    aptv: str = Query(None),
    fcc: str = Query(None),
):
    if file not in FILE_MAP:
        return Response("file 参数必须是 ct / cmcc / cu", status_code=400)

    # ✅ 动态获取当前访问域名
    base_url = get_base_url(request)
    m3u8_url = f"{base_url}/home/{FILE_MAP[file]}"

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(m3u8_url)

    if resp.status_code != 200:
        return Response(f"m3u8 文件不存在: {m3u8_url}", status_code=404)

    m3u_text = resp.text

    # IP 替换
    m3u_text = m3u_text.replace(DEFAULT_IP, ip)

    if aptv:
        m3u_text = m3u_text.replace(
            "{utc:YmdHMS}-{utcend:YmdHMS}",
            "${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}"
        )

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
            "Access-Control-Allow-Origin": "*"
        }
    )
