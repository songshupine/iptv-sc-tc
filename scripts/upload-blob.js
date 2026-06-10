import { getStore } from "@edgeone/pages";
import { readFileSync } from "fs";
import { join } from "path";

const store = getStore({
  name: "iptv-m3u8", // ← 你的 Blob namespace
  projectId: process.env.PAGES_PROJECT_ID,
  token: process.env.PAGES_API_TOKEN,
});

const files = [
  { key: "hls/live.m3u8", type: "application/vnd.apple.mpegurl" },
  { key: "hls/index.txt", type: "text/plain" },
];

for (const { key, type } of files) {
  const content = readFileSync(join("dist", key));

  await store.set(key, content, {
    contentType: type,
  });

  console.log(`✅ Uploaded ${key}`);
}

