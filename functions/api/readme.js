export const runtime = "edge";

import MarkdownIt from "markdown-it";
import markdownItTable from "markdown-it-table";
import { getStore } from "@edgeone/pages-blob";

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
}).use(markdownItTable);

export async function onRequest() {
  try {
    const store = getStore("iptv-m3u8");
    const blob = await store.get("home/readme.md");

    if (!blob) {
      return new Response("README not found", { status: 404 });
    }

    const markdown = await blob.text();

    const html = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>IPTV README</title>
  <style>
    body { font-family: sans-serif; padding: 24px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ddd; padding: 8px; }
    th { background: #f5f5f5; }
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
      },
    });
  } catch (err) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 500 }
    );
  }
}
