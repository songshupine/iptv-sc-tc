import { getStore } from "@edgeone/pages";
import { readFileSync } from "fs";
import { join } from "path";

const store = getStore({
  name: "iptv-m3u8",
  projectId: process.env.PAGES_PROJECT_ID,
  token: process.env.PAGES_API_TOKEN,
});

const files = ["ct.m3u8", "cmcc.m3u8", "cu.m3u8"];

for (const file of files) {
  const content = readFileSync(
    join("public", "home", file)
  );

  await store.set(`home/${file}`, content, {
    contentType: "application/vnd.apple.mpegurl",
  });

  console.log(`✅ Uploaded home/${file}`);
}
