// functions/api/readme.js

export const runtime = "edge";

import MarkdownIt from "markdown-it";
import container from "markdown-it-container";
import { getStore } from "@edgeone/pages-blob";

// 1. 初始化 Markdown-it（逻辑不变）
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
}).use(container, "table");

export async function onRequest() {
  try {
    // 2. 从 Blob Store 读取文件（逻辑不变）
    const store = getStore("iptv-m3u8");
    const mdContent = await store.get("home/readme.md");

    if (!mdContent) {
      return new Response(
        JSON.stringify({ error: "readme.md not found in Blob home directory" }),
        { status: 404, headers: { "Content-Type": "application/json" } }
      );
    }

    // 3. Markdown 转 HTML（逻辑不变）
    const html = md.render(mdContent);

    // 4. ✅ 返回 JSON，适配 api.ts 的 ReadmeResponse 接口
    // ✅ 关键修改点：注入表格样式 & 补全 source 字段
    return new Response(
      JSON.stringify({
        html: `
          <style>
            table { border-collapse: collapse; width: 100%; margin: 1em 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f5f5f5; font-weight: bold; }
          </style>
          ${html}
        `,
        source: "https://tv.gotonas.com/api/readme" // 补全来源信息
      }),
      {
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Cache-Control": "no-cache",
        },
      }
    );
  } catch (err) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}
