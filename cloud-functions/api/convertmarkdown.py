# cloud-functions/api/convertmarkdown.py
import sys
import os
import json
import markdown  # 引入 markdown 模块

# 确保当前目录在搜索路径中（兼容 EdgeOne 环境）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main_handler(event, context):
    try:
        # 1. 获取请求方法
        if request.method != 'POST':
            return {
                "statusCode": 405,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Method Not Allowed"})
            }

        # 2. 获取 POST 请求的 body
        body = request.body
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        
        payload = json.loads(body)
        md_text = payload.get("markdown", "")

        # 3. 使用 markdown 模块转换
        # extensions 可以根据需要添加，如 'tables', 'fenced_code' 等
        html_content = markdown.markdown(md_text, extensions=['extra', 'codehilite', 'toc'])

        # 4. 返回 JSON 响应
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"html": html_content})
        }

    except Exception as e:
        # 捕获异常并返回错误信息，方便调试
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }
