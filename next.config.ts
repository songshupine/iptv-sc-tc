import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  trailingSlash: false, 
  async redirects() {
    return [
      {
        // 1. 匹配源路径（仅匹配 /udpxy）
        source: "/udpxy",
        
        // 2. 重定向目标路径
        destination: "/api/udpxy",
        
        // 3. 使用 301 永久重定向（对客户端和播放器缓存更友好）
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
