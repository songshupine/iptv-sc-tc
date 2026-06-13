// 声明使用 Edge Runtime
export const runtime = "edge";

// 1. 导入依赖（使用稳定兼容的容器插件）
import MarkdownIt from "markdown-it";
import container from "markdown-it-container";
import { getStore } from "@edgeone/pages-blob";

// 2. 初始化 Markdown-it
const md = new MarkdownIt({
  html: true,       // 允许 HTML 标签
  linkify: true,    // 自动识别链接
  typographer: true // 排版优化
}).use(container, "table"); // 使用 container 插件来支持表格

export async function onRequest() {
  try {
    // 3. 从 Blob Store 读取文件（采用早期版本的正确逻辑）
    const store = getStore("iptv-m3u8"); // 你的 Blob Store 名称
    const mdContent = await store.get("home/readme.md"); // 文件路径

    // 4. 错误处理
    if (!mdContent) {
      return new Response(
        JSON.stringify({ error: "readme.md not found in Blob home directory" }),
        { status: 404, headers: { "Content-Type": "application/json" } }
      );
    }

    // 5. Markdown 转 HTML（注意：mdContent 直接是字符串）
    const htmlContent = md.render(mdContent);

    // 6. 拼接完整 HTML 页面
    const html = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>IPTV README</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto; padding: 24px; line-height: 1.6; }
    table { border-collapse: collapse; width: 100%; margin: 16px 0; }
    th, td { border: 1px solid #ddd; padding: 8px; }
    th { background: #f5f5f5; }
    a { color: #0366d6; }
  </style>
</head>
<body>
  ${htmlContent}
</body>
</html>
`;

    // 7. 返回响应
    return new Response(html, {
      headers: { "Content-Type": "text/html; charset=utf-8" },
    });

  } catch (err) {
    // 8. 全局错误捕获
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}
