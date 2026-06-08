# cloud-functions/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 修改这里：加上 /api 前缀
@app.post("/api/convert-markdown")  
async def convert_markdown(payload: dict):
    md_text = payload.get("markdown", "")
    
    # 使用纯正则进行基础 Markdown 转换
    html_content = md_text
    html_content = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.*)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
    html_content = html_content.replace('\n', '<br>')
    
    return {"html": html_content}
