// functions/api/readme.js

export const runtime = "edge";

import MarkdownIt from "markdown-it";
import container from "markdown-it-container";
import { getStore } from "@edgeone/pages-blob";

// 1. 初始化 Markdown-it
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
}).use(container, "table");

export async function onRequest() {
  try {
    // 2. 从 Blob Store 读取文件
    const store = getStore("iptv-m3u8");
    const mdContent = await store.get("home/readme.md");

    if (!mdContent) {
      return new Response(
        JSON.stringify({ error: "readme.md not found in Blob home directory" }),
        { status: 404, headers: { "Content-Type": "application/json" } }
      );
    }

    // 3. Markdown 转 HTML
    const html = md.render(mdContent);

    // 4. ✅ 返回 JSON，适配 api.ts 的 ReadmeResponse 接口
    return new Response(
      JSON.stringify({
        html: html,
        source: "https://tv.gotonas.com/api/readme"
      }),
      {
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Cache-Control": "no-cache"
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
