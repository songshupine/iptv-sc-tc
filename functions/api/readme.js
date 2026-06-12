import { getStore } from "@edgeone/pages-blob";
import MarkdownIt from "markdown-it";

// 初始化 markdown 解析器
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
});

export async function onRequest(context) {
  try {
    // 从 Blob 存储读取 readme.md
    const store = getStore("iptv-m3u8");
    const mdContent = await store.get("home/readme.md");

    if (!mdContent) {
      return new Response(
        JSON.stringify({ error: "readme.md not found" }),
        {
          status: 404,
          headers: { "Content-Type": "application/json" },
        }
      );
    }

    // 每次都重新渲染，不使用任何缓存
    const html = md.render(mdContent);

    return new Response(
      JSON.stringify({ html, source: "blob-storage" }),
      {
        headers: {
          "Content-Type": "application/json",
          // 禁止 CDN / 浏览器缓存
          "Cache-Control": "no-cache, no-store, must-revalidate",
        },
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
}
