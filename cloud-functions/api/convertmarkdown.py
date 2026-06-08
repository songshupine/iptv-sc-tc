# cloud-functions/api/convertmarkdown.py
from fastapi import FastAPI
from pydantic import BaseModel
import markdown

app = FastAPI()

# 定义请求体模型，FastAPI 会自动解析 JSON 并进行类型校验
class MarkdownRequest(BaseModel):
    markdown: str

@app.post('/convertmarkdown')
async def convert_markdown(request: MarkdownRequest):
    """
    接收 Markdown 文本并转换为 HTML
    """
    try:
        md_text = request.markdown
        
        # 使用 markdown 库进行转换
        # extensions 启用了常用扩展：表格、代码块高亮、目录等
        html_content = markdown.markdown(
            md_text, 
            extensions=['tables', 'fenced_code', 'toc']
        )

        return {"html": html_content}

    except Exception as e:
        return {"error": str(e)}
