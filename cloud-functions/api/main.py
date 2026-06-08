# cloud-functions/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import markdown

app = FastAPI()

# 配置 CORS（同域调用通常不需要，但作为良好实践保留）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义 POST 接口，路由为 /api/convert-markdown
@app.post("/convert-markdown")
async def convert_markdown(payload: dict):
    md_text = payload.get("markdown", "")
    # 将 Markdown 转换为 HTML
    html_content = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])
    return {"html": html_content}
