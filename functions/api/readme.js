// 使用 Edge Runtime
export const runtime = "edge";

import MarkdownIt from "markdown-it";
import { tablePlugin } from "markdown-it-table";
import { getStore } from "@edgeone/pages-blob";

// 初始化 markdown-it（已修复 table 插件导出问题）
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
}).use(tablePlugin);

export async function onRequest() {
  try {
    const store = getStore("iptv-m3u8");

    const blob = await store.get("home/readme.md");
    if (!blob) {
      return new Response("README not found", { status: 404 });
    }

    const markdown = await blob.text();

    // 基础 HTML 模板（含表格样式）
    const html = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>IPTV README</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto;
      line-height: 1.6;
      padding: 24px;
      max-width: 960px;
      margin: auto;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 16px 0;
    }
    th, td {
      border: 1px solid #ddd;
      padding: 8px;
    }
    th {
      background: #f5f5f5;
    }
    a {
      color: #0366d6;
    }
  </style>
</head>
<body>
  ${md.render(markdown)}
</body>
</html>
`;

    return new Response(html, {
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-cache",
      },
    });
  } catch (err) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 500 }
    );
  }
}
