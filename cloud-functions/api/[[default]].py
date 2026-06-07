from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import markdown

app = FastAPI()

# 定义根目录路由
@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        # 读取 README.md 文件内容
        with open("README.md", "r", encoding="utf-8") as f:
            md_content = f.read()
        
        # 将 Markdown 转换为 HTML
        html_content = markdown.markdown(md_content)
        
        # 包装成完整的 HTML 结构返回
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>IPTV API Docs</title>
            <style>
                body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: auto; }}
                code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 4px; }}
                pre {{ background: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
    except FileNotFoundError:
        return "<h1>404 Not Found</h1><p>README.md not found.</p>", 404
