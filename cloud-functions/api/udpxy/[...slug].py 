from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# 这个路由会捕获所有请求，并返回详细的诊断信息
@app.api_route("/{full_path:path}", methods=["GET", "POST"])
async def debug_endpoint(request: Request, full_path: str = ""):
    # 1. 获取 Next.js 转发过来的原始路径
    original_path = request.url.path
    
    # 2. 获取所有的查询参数 (如 aptv=1, fcc=xxx)
    query_params = dict(request.query_params)
    
    # 3. 获取所有的请求头 (看看 Next.js 有没有加特殊的 Header)
    headers = dict(request.headers)
    
    # 4. 组装诊断信息
    debug_info = {
        "message": "Python 云函数已成功接收请求！",
        "received_full_path": full_path,
        "original_request_path": original_path,
        "query_params": query_params,
        "request_headers": headers
    }
    
    # 以 JSON 格式返回，方便在浏览器中直接查看
    return JSONResponse(content=debug_info)
