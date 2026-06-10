import { readFileSync } from "fs";
import { join } from "path";

const PROJECT_ID = process.env.PAGES_PROJECT_ID;
const API_TOKEN = process.env.PAGES_API_TOKEN;

const files = ["ct.m3u8", "cmcc.m3u8", "cu.m3u8"];

for (const file of files) {
  const content = readFileSync(join("public", "home", file));

  const res = await fetch(
    `https://api.edgeone.ai/v1/projects/${PROJECT_ID}/stores/iptv-m3u8/objects/home/${file}`,
    {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${API_TOKEN}`,
        "Content-Type": "application/vnd.apple.mpegurl",
      },
      body: content,
    }
  );

  if (!res.ok) {
    throw new Error(`Upload failed: ${file} ${res.status}`);
  }

  console.log(`✅ Uploaded home/${file}`);
}
