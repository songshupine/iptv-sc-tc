import { getStore } from "@edgeone/pages-blob";
import { readFileSync } from "fs";
import { join } from "path";

const store = getStore({
  name: "iptv-m3u8",
  projectId: process.env.PAGES_PROJECT_ID,
  token: process.env.PAGES_API_TOKEN,
});

// ✅ 原有 m3u8 文件
const files = ["ct.m3u8", "cmcc.m3u8", "cu.m3u8"];

// ✅ README.md 在 GitHub 项目根目录
const readmePath = join(process.cwd(), "README.md");

// 1️⃣ 上传 m3u8
for (const file of files) {
  const content = readFileSync(join("public", "home", file));
  await store.set(`home/${file}`, content, {
    contentType: "application/vnd.apple.mpegurl",
  });
  console.log(`✅ Uploaded home/${file}`);
}

// 2️⃣ 上传 README.md
try {
  const readmeContent = readFileSync(readmePath);
  await store.set("home/readme.md", readmeContent, {
    contentType: "text/markdown",
  });
  console.log(`✅ Uploaded home/readme.md`);
} catch (e) {
  console.warn("⚠️ README.md not found or upload failed:", e.message);
}
