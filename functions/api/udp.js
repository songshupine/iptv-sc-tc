// functions/api/udpxy.js
import { getStore } from "@edgeone/pages-blob";

// -----------------------------
// 不同 file 的映射配置（从 Python 翻译）
// -----------------------------
const FILE_CONFIG = {
  ct: {
    m3u8: "ct.m3u8",
    time_pattern: "{utc:YmdHMS}-{utcend:YmdHMS}",
    time_replace: "${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}",
    catchup_proto: "rtsp",
  },
  cmcc: {
    m3u8: "cmcc.m3u8",
    time_pattern: "{utc:YmdHMS}/{utcend:YmdHMS}",
    time_replace: "${(b)yyyyMMddHHmmss}/${(e)yyyyMMddHHmmss}",
    catchup_proto: "http",
  },
  cu: {
    m3u8: "cu.m3u8",
    time_pattern: "{utc:YmdHMS}-{utcend:YmdHMS}",
    time_replace: "${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}",
    catchup_proto: "rtsp",
  },
};

const DEFAULT_IP = "192.168.100.1:4022";

/**
 * Edge Function 主入口
 * 访问路径：/api/udpxy?file=ct&ip=xxx...
 */
export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);

  // 1. 解析 Query 参数
  const file = url.searchParams.get("file");
  const txt = url.searchParams.get("txt") || "1";
  const ip = url.searchParams.get("ip") || DEFAULT_IP;
  const aptv = url.searchParams.get("aptv");
  const fcc = url.searchParams.get("fcc");
  const r2hToken = url.searchParams.get("r2h-token");
  const httpProxy = url.searchParams.get("httpProxy");
  const rtspProxy = url.searchParams.get("rtspProxy");

  if (!FILE_CONFIG[file]) {
    return new Response("file 必须为 ct / cmcc / cu", { status: 400 });
  }

  const cfg = FILE_CONFIG[file];

  // 2. ✅ 从 Blob 存储获取 m3u8（核心改造点）
  const store = getStore("iptv-m3u8"); // 替换为你的 Blob Store 名称
  const m3u8Key = `home/${cfg.m3u8}`; // 假设 m3u8 在 Blob 的 home 目录下

  try {
    const m3uText = await store.get(m3u8Key);
    if (!m3uText) {
      return new Response(`Blob 中未找到文件: ${m3u8Key}`, { status: 404 });
    }

    let processedText = m3uText;

    // 3. IP 替换
    processedText = processedText.replace(DEFAULT_IP, ip);

    // 4. APTV 时间占位符
    if (aptv) {
      processedText = processedText.replace(
        cfg.time_pattern,
        cfg.time_replace
      );
    }

    // 5. FCC 追加
    if (fcc) {
      const lines = processedText.split("\n");
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes("/udp/")) {
          const sep = lines[i].includes("?") ? "&" : "?";
          lines[i] += `${sep}fcc=${fcc}`;
        }
      }
      processedText = lines.join("\n");
    }

    // 6. r2h-token
    if (r2hToken) {
      const lines = processedText.split("\n");
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes("/udp/") || lines[i].includes("playseek=")) {
          const sep = lines[i].includes("?") ? "&" : "?";
          lines[i] += `${sep}r2h-token=${r2hToken}`;
        }
      }
      processedText = lines.join("\n");
    }

    // 7. Catchup Proxy
    const proxy = httpProxy || rtspProxy;
    if (proxy) {
      const proto = cfg.catchup_proto;
      const lines = processedText.split("\n");
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes(`catchup-source="${proto}://`)) {
          lines[i] = lines[i].replace(
            `catchup-source="${proto}://`,
            `catchup-source="${proxy}/${proto}/`
          );
        }
      }
      processedText = lines.join("\n");
    }

    // 8. 返回响应
    return new Response(processedText, {
      headers: {
        "Content-Type": txt === "0"
          ? "text/plain; charset=utf-8" //"application/vnd.apple.mpegurl"
          : "text/plain; charset=utf-8",
        "Cache-Control": "no-cache",
        "Access-Control-Allow-Origin": "*",
      },
    });

  } catch (error) {
    return new Response(`Blob 读取失败: ${error.message}`, { status: 500 });
  }
}

