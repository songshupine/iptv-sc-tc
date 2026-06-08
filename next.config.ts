import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 强制关闭尾部斜杠，防止 308 重定向
  trailingSlash: false, 
  async rewrites() {
    return [
      {
        // 匹配 /udpxy/ 后面的所有内容（包括 IP:Port）
        source: "/udpxy/:path*",
        // 【关键】直接透传 :path*，Next.js 不会去解析里面的冒号和点
        destination: "/api/udpxy/:path*", 
      },
    ];
  },
};

export default nextConfig;
