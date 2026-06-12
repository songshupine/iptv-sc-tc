// functions/api/readme.js
import { getStore } from "@edgeone/pages-blob";
import MarkdownIt from "markdown-it";

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
});

// 缓存配置
const CACHE_TTL = 60 * 1000; // 1 分钟
let memoryCache = null;
let cacheTime = 0;

export async function onRequest(context) {
  try {
    // 1. 内存缓存检查
    //if (memoryCache && Date.now() - cacheTime < CACHE_TTL) {
    //  return new Response(
    //    JSON.stringify({ html: memoryCache, source: "memory-cache" }),
    //    { headers: { "Content-Type": "application/json" } }
    //  );
    //}

    // 2. ✅ 从 Blob 的 home 目录读取 readme.md
    const store = getStore("iptv-m3u8"); // 替换为你的 Blob Store 名称
    const mdContent = await store.get("home/readme.md"); // ← 修改点

    if (!mdContent) {
      return new Response(
        JSON.stringify({ error: "readme.md not found in Blob home directory" }),
        { status: 404 }
      );
    }

    // 3. Markdown 转 HTML
    const html = md.render(mdContent);

    // 4. 更新缓存
    memoryCache = html;
    cacheTime = Date.now();

    return new Response(
      JSON.stringify({ html, source: "blob-storage" }),
      {
        headers: {
          "Content-Type": "application/json",
          "Cache-Control": "public, max-age=60",
        },
      }
    );

  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500 }
    );
  }
}
