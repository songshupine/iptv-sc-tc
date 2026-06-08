from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# 捕获所有 GET 请求
@app.get("/{full_path:path}")
async def debug_endpoint(request: Request, full_path: str = ""):
    return JSONResponse({
        "message": "Python 云函数已成功接收请求！",
        "received_path": full_path,
        "original_url": str(request.url),
        "query_params": dict(request.query_params)
    })
